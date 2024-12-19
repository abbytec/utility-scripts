// unhandledRejectionExample.js

// Configurar el manejador para 'unhandledRejection'
process.on('unhandledRejection', (reason, promise) => {
  console.log('--- Evento "unhandledRejection" activado ---');
  console.log('Razón del rechazo (reason):', reason);
  console.log('Promesa rechazada (promise):', promise);
  console.log('-------------------------------------------');
});

// Función que retorna una promesa que se rechaza
function promesaRechazada() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      reject(new Error('¡Esta promesa fue rechazada sin manejar!'));
    }, 1000); // Rechaza después de 1 segundo
  });
}

// Ejecutar la función sin manejar el rechazo
promesaRechazada();

// También puedes desencadenar otro tipo de rechazo, como rechazar directamente
Promise.reject('Rechazo directo sin manejo');

// Nota: No usamos .catch() ni async/await para manejar los rechazos

