import { 
    getStudentbyQRCode, 
    registerReading, 
    registerFrequency, 
    registerSnack 
} from '../api.js';

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true });
const statusEl = document.getElementById('status');
const logEl = document.getElementById('log');
const box = document.getElementById('camera-box');

let stream = null;
let scanning = false;
let animationId = null;
let isProcessing = false; // Trava para evitar leituras duplicadas simultâneas

function log(msg) {
    const item = document.createElement('div');
    item.textContent = new Date().toLocaleTimeString() + ' — ' + msg;
    logEl.prepend(item);
}

async function sendReading(student) {
    const dataReading = {
        student: student.id,
        moment: "LUNCH"
    };

    const response = await registerReading(dataReading);
    if (response && (response.status === 201 || response.status === 200)) {
        log('Leitura registrada com sucesso!');
        return response.dados;
    } else {
        log('Erro ao registrar leitura.');
        return null;
    }
}

async function sendFrequency(studentId, readingId) {
    const dataFrequency = {
        student: studentId,
        date: new Date().toISOString().split('T')[0],
        on_time: true,
        reading: readingId
    };

    const response = await registerFrequency(dataFrequency);
    if (response && (response.status === 201 || response.status === 200)) {
        log('Frequência registrada com sucesso!');
        return response.dados;
    } else {
        log('Erro ao registrar frequência.');
        return null;
    }
}

async function sendRegisterSnack(studentId, type_snack, readingId) {
    const dataSnack = {
        student: studentId,
        date: new Date().toISOString().split('T')[0],
        moment: "LUNCH",
        type_snack: type_snack,
        reading: readingId
    };

    const response = await registerSnack(dataSnack);
    if (response && (response.status === 201 || response.status === 200)) {
        log('Lanche registrado com sucesso!');
        return response.dados;
    } else {
        log('Erro ao registrar lanche.');
        return null;
    }
}

async function processQRCode(qrData) {
    isProcessing = true;
    statusEl.textContent = 'Processando leitura...';

    try {
        log(`Buscando aluno do QR: ${qrData}`);
        const student = await getStudentbyQRCode(qrData);
        console.log('student', student, "qrData", qrData);

        if (student && student.id) {
            log(`Aluno: ${student.name || student.id}`);

            // 1. Registra leitura
            const reading = await sendReading(student);

            if (reading && reading.id) {
                console.log('reading', reading);
                // 2. Registra frequência
                await sendFrequency(student.id, reading.id);
                console.log('Frequência registrada para o aluno:', student.name || student.id);

                const { wantsSnack, wantsLunch, lunchType: chosenLunchType } =
                await askMealPreferences(student.name);

                // 3. Registra lanche
                await sendRegisterSnack(student.id, "STANDARD", reading.id);
                console.log('Lanche registrado para o aluno:', student.name || student.id);
            }
        } else {
            log('Aluno não encontrado para este QR Code.');
        }
    } catch (error) {
        console.error(error);
        log('Erro ao processar requisições do QR Code.');
    } finally {
        // Pausa de 3 segundos para o usuário afastar o QR Code antes de ler o próximo
        setTimeout(() => {
            isProcessing = false;
            statusEl.textContent = 'Procurando QR code...';
        }, 3000);
    }
}

async function ligarCamera() {
    try {
        statusEl.textContent = 'Ligando câmera...';
        stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment' },
            audio: false
        });
        video.srcObject = stream;
        await video.play();
        box.style.borderColor = '#28a745';
        statusEl.textContent = 'Procurando QR code...';
        scanning = true;
        tick();
    } catch (erro) {
        statusEl.textContent = 'Erro ao acessar câmera: ' + erro.message;
        console.error(erro);
    }
}

function desligarCamera() {
    scanning = false;
    if (animationId) cancelAnimationFrame(animationId);
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    box.style.borderColor = '#ccc';
    statusEl.textContent = 'Câmera desligada.';
}

function tick() {
    if (!scanning) return;

    if (video.readyState === video.HAVE_ENOUGH_DATA && !isProcessing) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: 'dontInvert'
        });

        if (code && code.data) {
            log('QR lido: ' + code.data);
            processQRCode(code.data);
        }
    }

    animationId = requestAnimationFrame(tick);
}

ligarCamera();