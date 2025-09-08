const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Function to parse a single HTML file
function parseHTMLFile(filePath) {
  const htmlContent = fs.readFileSync(filePath, 'utf-8');
  const dom = new JSDOM(htmlContent);
  const document = dom.window.document;
  
  const messages = [];
  let lastSender = '';
  
  // Get all message elements (both regular and joined)
  const messageElements = document.querySelectorAll('.message.default.clearfix, .message.default.clearfix.joined');
  
  console.log(`Found ${messageElements.length} message elements in ${path.basename(filePath)}`);
  
  messageElements.forEach((element, index) => {
    try {
      const id = element.getAttribute('id').replace('message-', '');
      
      // Extract date
      const dateElement = element.querySelector('.pull_right.date.details');
      const date = dateElement ? dateElement.getAttribute('title') : '';
      
      // Extract sender
      let sender = '';
      const fromElement = element.querySelector('.from_name');
      if (fromElement) {
        sender = fromElement.textContent.trim();
        lastSender = sender; // Update last sender
      } else if (element.classList.contains('joined')) {
        // For joined messages, use the last sender
        sender = lastSender;
      }
      
      // Extract text
      let text = '';
      const textElement = element.querySelector('.text');
      if (textElement) {
        // Get all text content, including nested elements
        text = textElement.textContent.trim();
      }
      
      // Skip messages without text
      if (!text) {
        return;
      }
      
      // Create origin URL
      const origin = `https://t.me/flutterflow_rus/chat_export/${id}`;
      
      // Create a mock embedding (in a real scenario, you would generate actual embeddings)
      const embedding = Array(1536).fill(0).map(() => Math.random() * 0.1 - 0.05);
      
      messages.push({
        id: parseInt(id),
        date,
        sender,
        text,
        origin,
        embedding
      });
      
      // Log progress for large files
      if ((index + 1) % 1000 === 0) {
        console.log(`  Processed ${index + 1} messages...`);
      }
    } catch (error) {
      console.error(`Error parsing message ${index} in ${filePath}:`, error.message);
    }
  });
  
  return messages;
}

// Main function to process all HTML files
function processChatExport(inputDir, outputFile) {
  const allMessages = [];
  const htmlFiles = fs.readdirSync(inputDir).filter(file => file.startsWith('messages') && file.endsWith('.html'));
  
  console.log(`Found ${htmlFiles.length} HTML files to process`);
  
  htmlFiles.forEach((file, index) => {
    const filePath = path.join(inputDir, file);
    console.log(`Processing ${file} (${index + 1}/${htmlFiles.length})`);
    
    try {
      const messages = parseHTMLFile(filePath);
      allMessages.push(...messages);
      console.log(`  Extracted ${messages.length} messages`);
    } catch (error) {
      console.error(`Error processing ${file}:`, error.message);
    }
  });
  
  console.log(`Total messages extracted: ${allMessages.length}`);
  
  // Sort messages by ID
  allMessages.sort((a, b) => a.id - b.id);
  
  // Remove duplicates (in case any messages appear in multiple files)
  const uniqueMessages = [];
  const seenIds = new Set();
  
  for (const message of allMessages) {
    if (!seenIds.has(message.id)) {
      seenIds.add(message.id);
      uniqueMessages.push(message);
    }
  }
  
  console.log(`Unique messages after deduplication: ${uniqueMessages.length}`);
  
  // Write to output file
  fs.writeFileSync(outputFile, JSON.stringify(uniqueMessages, null, 2));
  console.log(`Output written to ${outputFile}`);
  
  return uniqueMessages;
}

// Run the script
const inputDir = path.join(__dirname, '..', 'ChatExport_2025-09-03-v1');
const outputFile = path.join(__dirname, '..', 'base3y.json');

const messages = processChatExport(inputDir, outputFile);
console.log(`Final output contains ${messages.length} messages`);