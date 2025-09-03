
import * as fs from 'fs';
import * as path from 'path';
import * as cheerio from 'cheerio';

interface Message {
  id: number;
  date: string;
  sender: string;
  text: string;
  origin: string;
}

const CHAT_EXPORT_DIR = '/Users/eugene/MyProjects/ff-base-ai-search/ChatExport_2025-09-03';
const OUTPUT_FILE = '/Users/eugene/MyProjects/ff-base-ai-search/knowledge_base.json';

const messages: Message[] = [];

// Function to find the topic ID from a file's content
const findTopicId = ($: cheerio.CheerioAPI): string | null => {
  const replyLinks = $('.reply_to a');
  for (let i = 0; i < replyLinks.length; i++) {
    const el = replyLinks[i];
    const href = $(el).attr('href');
    if (href && href.includes('messages.html#go_to_message')) {
      const match = href.match(/go_to_message(\d+)/);
      if (match && match[1]) {
        return match[1]; // Return immediately when found
      }
    }
  }
  return null; // Return null if not found after checking all links
};

// Function to sanitize chat name for URL
const sanitizeChatName = (name: string): string => {
    return name
        .trim()
        .replace(/🌀/g, '') // Remove emoji
        .trim() // Trim again in case of spaces around emoji
        .replace(/\s+/g, '_') // Replace spaces with a single underscore
        .replace(/[^a-zA-Z0-9_]+/g, '') // Remove any remaining non-alphanumeric characters (except underscore)
        .toLowerCase();
};


try {
  const files = fs.readdirSync(CHAT_EXPORT_DIR).filter(file => file.endsWith('.html'));

  for (const file of files) {
    const filePath = path.join(CHAT_EXPORT_DIR, file);
    const html = fs.readFileSync(filePath, 'utf-8');
    const $ = cheerio.load(html);

    const chatNameRaw = $('.page_header .text.bold').first().text();
    const chatName = sanitizeChatName(chatNameRaw);
    
    const topicId = findTopicId($);

    if (!topicId) {
        console.warn(`Could not find a topic_id in ${file}. Skipping messages in this file.`);
        continue;
    }

    $('.message.default').each((i, el) => {
      const idAttr = $(el).attr('id');
      if (!idAttr) return;

      const id = parseInt(idAttr.replace('message', ''), 10);
      const date = $('.pull_right.date.details', el).attr('title') || '';
      const sender = $('.from_name', el).text().trim();
      const text = $('.text', el).text().trim();
      
      if (id && date && sender && text) {
        const origin = `https://t.me/${chatName}/${topicId}/${id}`;
        messages.push({ id, date, sender, text, origin });
      }
    });
  }

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(messages, null, 2));
  console.log(`Successfully parsed ${messages.length} messages.`);
  console.log(`Output saved to ${OUTPUT_FILE}`);

} catch (error) {
  console.error('An error occurred during parsing:', error);
}
