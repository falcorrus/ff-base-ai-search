// run-generate-embeddings.js
const { exec } = require('child_process');

// Запуск скомпилированного скрипта генерации эмбеддингов
exec('node dist/scripts/generateEmbeddings.js', (error, stdout, stderr) => {
  if (error) {
    console.error(`Ошибка выполнения: ${error}`);
    return;
  }
  
  if (stderr) {
    console.error(`Ошибка stderr: ${stderr}`);
  }
  
  console.log(`stdout: ${stdout}`);
});