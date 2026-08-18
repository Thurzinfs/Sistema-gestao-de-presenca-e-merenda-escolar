const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true });
const statusEl = document.getElementById('status');
const logEl = document.getElementById('log');
const box = document.getElementById('camera-box');

let stream = null;
let scanning = false;
let animationId = null;

function log(msg) {
const item = document.createElement('div');
item.textContent = new Date().toLocaleTimeString() + ' — ' + msg;
logEl.prepend(item);
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

if (video.readyState === video.HAVE_ENOUGH_DATA) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(imageData.data, imageData.width, imageData.height, {
    inversionAttempts: 'dontInvert'
    });

    if (code && code.data) {
    console.log(code.data);
    log('QR lido: ' + code.data);

    desligarCamera();
    setTimeout(ligarCamera, 1000000); // adidciona aqui o codigo da requisicao
    return;
    }
}

animationId = requestAnimationFrame(tick);
}

ligarCamera();
