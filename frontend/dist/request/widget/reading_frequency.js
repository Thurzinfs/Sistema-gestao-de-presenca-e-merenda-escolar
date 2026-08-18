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

const cardStats = document.getElementById('card-stats');
const cardMessage = document.getElementById('card-message');
const cardFund = document.getElementById('card-fund');
const cardStatus = document.getElementById('card-status');

const nameEl = document.getElementById('name');
const btnEnviar = document.getElementById('btn-enviar');

function showCards() {
    cardStats?.classList.remove('d-none');
    cardMessage?.classList.remove('d-none');
    cardFund?.classList.remove('d-none');
    cardStatus?.classList.remove('d-none');
}

function hideCards() {
    cardStats?.classList.add('d-none');
    cardMessage?.classList.add('d-none');
    cardFund?.classList.add('d-none');
    cardStatus?.classList.add('d-none');
}

let stream = null;
let scanning = false;
let animationId = null;
let isProcessing = false; // Trava para evitar leituras duplicadas simultâneas

// Guarda o aluno e a leitura atual, aguardando o clique em "Enviar"
let currentStudent = null;
let currentReading = null;

function log(msg) {
    const item = document.createElement('div');
    item.textContent = new Date().toLocaleTimeString() + ' — ' + msg;
    logEl.prepend(item);
}

async function sendReading(student) {
    const dataReading = {
        student: student,
        moment: "LUNCH"
    };

    const response = await registerReading(dataReading);
    if (response && (response.status === 201 || response.status === 200)) {
        log('Leitura registrada com sucesso!');
        return response.dados;
    } else {
        log('Leitura ja Registrada.');
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

async function sendRegisterSnack(studentId, type_snack, readingId, moment = "LUNCH") {
    const dataSnack = {
        student: studentId,
        date: new Date().toISOString().split('T')[0],
        moment: moment,
        type_snack: type_snack,
        reading: readingId
    };

    const response = await registerSnack(dataSnack);
    if (response && (response.status === 201 || response.status === 200)) {
        log('Registro enviado com sucesso!');
        return response.dados;
    } else {
        log('Erro ao registrar.');
        return null;
    }
}

function resetToScanning() {
    currentStudent = null;
    currentReading = null;
    hideCards();
    isProcessing = false;
    statusEl.textContent = 'Procurando QR code...';
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
            const reading = await sendReading(student.id);

            if (reading && reading.id) {
                console.log('reading', reading);

                // Guarda para uso no clique de "Enviar"
                currentStudent = student;
                currentReading = reading;

                if (nameEl) {
                    nameEl.textContent = student.name || student.id;
                }

                showCards();

                // 2. Registra frequência (automático)
                await sendFrequency(student.id, reading.id);
                console.log('Frequência registrada para o aluno:', student.name || student.id);

                statusEl.textContent = 'Selecione as opções e clique em Enviar.';
                return; // aguarda a ação do usuário no botão Enviar
            }
        } else {
            log('Aluno não encontrado para este QR Code.');
        }
    } catch (error) {
        console.error(error);
        log('Erro ao processar requisições do QR Code.');
    }

    // Só libera a próxima leitura automaticamente se não chegou a exibir o card
    setTimeout(() => {
        isProcessing = false;
        statusEl.textContent = 'Procurando QR code...';
    }, 3000);
}

// Ação do botão "Enviar"
btnEnviar?.addEventListener('click', async () => {
    if (!currentStudent || !currentReading) {
        log('Nenhum aluno pendente para envio.');
        return;
    }

    btnEnviar.disabled = true;

    try {
        const wantsSnack = document.getElementById('lanchar-sim')?.checked;
        const lunchType = document.getElementById('almoco-pouco')?.checked ? 'POUCO' : 'NORMAL';

        // Lanche (só envia se "Sim")
        if (wantsSnack) {
            await sendRegisterSnack(currentStudent.id, 'NORMAL', currentReading.id, 'SNACK');
        }

        // Almoço (Pouco ou Normal)
        await sendRegisterSnack(currentStudent.id, lunchType, currentReading.id, 'LUNCH');

        log(`Preferências enviadas: Lanche = ${wantsSnack ? 'Sim' : 'Não'}, Almoço = ${lunchType}`);
    } catch (error) {
        console.error(error);
        log('Erro ao enviar preferências.');
    } finally {
        btnEnviar.disabled = false;
        setTimeout(() => {
            resetToScanning();
        }, 1500);
    }
});

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