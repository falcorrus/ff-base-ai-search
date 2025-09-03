// src/scripts/parseTelegramChat.ts
import * as fs from 'fs';
import * as path from 'path';
import * as cheerio from 'cheerio';

// Путь к директории с экспортированным чатом
const chatDir = path.resolve(__dirname, '../../../ChatExport_2025-09-03');
// Путь к файлу векторной базы данных
const vectorDbPath = path.resolve(__dirname, '../../data/vector-db.json');

interface TelegramMessage {
  id: string;
  path: string;
  title: string;
  content: string;
  createdAt: string;
  updatedAt: string;
  embedding: number[];
}

async function parseTelegramChat(): Promise<void> {
  console.log('Начинаем парсинг Telegram чата...');
  
  try {
    // Читаем все HTML-файлы из директории чата
    const htmlFiles = fs.readdirSync(chatDir).filter(file => file.startsWith('messages') && file.endsWith('.html'));
    console.log(`Найдено ${htmlFiles.length} файлов для обработки`);
    
    const allMessages: TelegramMessage[] = [];
    let messageId = 1;
    
    // Обрабатываем каждый HTML-файл
    for (const file of htmlFiles) {
      console.log(`Обрабатываем файл: ${file}`);
      const filePath = path.join(chatDir, file);
      const htmlContent = fs.readFileSync(filePath, 'utf8');
      const $ = cheerio.load(htmlContent);
      
      // Ищем все сообщения в файле
      $('.message.default').each((index, element) => {
        try {
          const $message = $(element);
          const id = $message.attr('id')?.replace('message-', '') || `${messageId}`;
          
          // Получаем дату сообщения
          const dateElement = $message.find('.pull_right.date.details');
          const dateTitle = dateElement.attr('title');
          let createdAt = new Date().toISOString();
          if (dateTitle) {
            // Пытаемся распарсить дату
            const dateMatch = dateTitle.match(/(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})/);
            if (dateMatch) {
              const dateStr = dateMatch[1];
              // Преобразуем формат даты из DD.MM.YYYY HH:mm:ss в ISO
              const [datePart, timePart] = dateStr.split(' ');
              const [day, month, year] = datePart.split('.');
              const isoDateStr = `${year}-${month}-${day}T${timePart}.000Z`;
              createdAt = new Date(isoDateStr).toISOString();
            }
          }
          
          // Получаем имя отправителя
          const fromName = $message.find('.from_name').text().trim() || 'Неизвестный пользователь';
          
          // Получаем текст сообщения
          let content = $message.find('.text').text().trim();
          
          // Если нет текста, проверяем другие возможные элементы
          if (!content) {
            content = $message.find('.media_wrap .media_caption').text().trim();
          }
          
          // Пропускаем пустые сообщения
          if (!content) {
            return;
          }
          
          // Создаем объект сообщения
          const message: TelegramMessage = {
            id: `${messageId}`,
            path: `chat/${file}#${id}`,
            title: `Сообщение от ${fromName}`,
            content: content,
            createdAt: createdAt,
            updatedAt: createdAt,
            embedding: []
          };
          
          allMessages.push(message);
          messageId++;
        } catch (error) {
          console.error(`Ошибка при обработке сообщения в файле ${file}:`, error);
        }
      });
    }
    
    console.log(`Всего обработано сообщений: ${allMessages.length}`);
    
    // Загружаем существующую векторную базу данных
    let existingData: TelegramMessage[] = [];
    if (fs.existsSync(vectorDbPath)) {
      const existingContent = fs.readFileSync(vectorDbPath, 'utf8');
      existingData = JSON.parse(existingContent);
      console.log(`Загружено ${existingData.length} существующих записей`);
    }
    
    // Объединяем существующие данные с новыми сообщениями
    // Удаляем дубликаты по ID
    const combinedData = [...existingData];
    const existingIds = new Set(existingData.map(item => item.id));
    
    for (const message of allMessages) {
      if (!existingIds.has(message.id)) {
        combinedData.push(message);
      }
    }
    
    console.log(`Итоговое количество записей в базе: ${combinedData.length}`);
    
    // Сохраняем обновленную векторную базу данных
    fs.writeFileSync(vectorDbPath, JSON.stringify(combinedData, null, 2), 'utf8');
    console.log(`Векторная база данных успешно обновлена: ${vectorDbPath}`);
    
    // Создаем отчет
    console.log('\n--- Отчет ---');
    console.log(`Добавлено новых сообщений: ${combinedData.length - existingData.length}`);
    console.log(`Всего сообщений в базе: ${combinedData.length}`);
    
  } catch (error) {
    console.error('Ошибка при парсинге Telegram чата:', error);
  }
}

// Запускаем парсинг
parseTelegramChat();