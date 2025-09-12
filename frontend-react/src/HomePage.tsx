import React, { useState, useEffect, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import { PlaceholdersAndVanishInput } from "./components/ui/placeholders-and-vanish-input";
import { motion } from "framer-motion";

const HomePage = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedDocument, setSelectedDocument] = useState<any | null>(null);

  const resetSearch = useCallback(() => {
    setQuery('');
    setResult('');
    setDocuments([]);
    setError('');
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (selectedDocument) {
          setSelectedDocument(null);
        } else if (result || query || error) {
          resetSearch();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [selectedDocument, result, query, error, resetSearch]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    setError('');
    setResult('');
    setDocuments([]);

    try {
      const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setResult(data.answer);
      setDocuments(data.relevant_documents || []);
    } catch (e: any) {
      setError(`Failed to fetch search results: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-900 via-blue-900 to-indigo-900 text-white overflow-hidden">
      {/* Анимированный фон с облаками */}
      <div className="absolute inset-0 z-0 overflow-hidden">
        {[...Array(8)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute rounded-full opacity-20"
            style={{
              background: `radial-gradient(ellipse at center, ${
                i % 3 === 0 ? '#93c5fd' : 
                i % 3 === 1 ? '#a5b4fc' : 
                '#60a5fa'
              } 0%, transparent 70%)`,
              width: `${200 + i * 150}px`,
              height: `${80 + i * 40}px`,
              top: `${5 + i * 12}%`,
              left: `${i * 15}%`,
            }}
            animate={{ x: [0, 100, 0, -100, 0], y: [0, -20, 0, 20, 0]}}
            transition={{ duration: 25 + i * 5, repeat: Infinity, ease: "easeInOut"}}
          />
        ))}
        {[...Array(15)].map((_, i) => (
          <motion.div
            key={`small-${i}`}
            className="absolute rounded-full opacity-15"
            style={{
              background: `radial-gradient(ellipse at center, #bfdbfe 0%, transparent 70%)`,
              width: `${30 + i * 10}px`,
              height: `${15 + i * 5}px`,
              top: `${20 + (i * 5) % 80}%`,
              left: `${(i * 7) % 100}%`,
            }}
            animate={{ x: [0, 50, 0, -50, 0]}}
            transition={{ duration: 20 + i * 2, repeat: Infinity, ease: "easeInOut"}}
          />
        ))}
      </div>

      {/* Основной контент */}
      <div className={`relative z-10 flex flex-col items-center min-h-screen px-4 transition-all duration-500 ${loading || result || error ? 'justify-start pt-28' : 'justify-center py-12'}`}>
        
        {/* Заголовок (скрывается при поиске) */}
        {!loading && !result && !error && (
          <div className="text-center mb-8 mt-8">
            <motion.div
              className="flex justify-center mb-8"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 260, damping: 20, delay: 0.2}}
            >
              <div className="relative">
                <div className="absolute -inset-4 bg-gradient-to-r from-sky-400 to-blue-500 rounded-full blur-lg opacity-75 animate-pulse"></div>
                <div className="relative bg-gradient-to-r from-sky-500 to-blue-600 p-6 rounded-full shadow-2xl">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                  </svg>
                </div>
              </div>
            </motion.div>
            <motion.h1 
              className="text-5xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-sky-200 via-blue-200 to-indigo-200"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              Интеллектуальный <span className="block">поиск по заметкам</span>
            </motion.h1>
          </div>
        )}

        {/* Форма поиска */}
        <motion.div
          className="w-full max-w-6xl mb-20"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.8 }}
        >
          <PlaceholdersAndVanishInput
            placeholders={[
              "Как настроить синхронизацию Google Drive?",
              "Настройка Cloud Functions",
              "Примеры использования Google Gemini API",
              "Как работает векторный поиск?",
              "Развертывание FastAPI на Google Cloud Run",
            ]}
            onChange={(e) => setQuery(e.target.value)}
            onSubmit={handleSearch}
            onClear={resetSearch}
            value={query}
          />
        </motion.div>

        {/* Блок результатов */}
        <div className="w-full max-w-6xl mb-20 px-4">
          {loading && (
            <div className="flex justify-center items-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sky-300"></div>
            </div>
          )}
          {error && (
            <div className="bg-red-900/50 border border-red-500 text-red-300 p-4 rounded-lg">
              <p>Ошибка: {error}</p>
            </div>
          )}
          {result && (
            <motion.div 
              className="bg-sky-900/60 backdrop-blur-md border border-sky-300/30 p-6 rounded-lg"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <h3 className="text-2xl font-bold mb-4 text-sky-200">Результат поиска:</h3>
              <p className="text-lg text-white whitespace-pre-wrap">{result}</p>
              {documents.length > 0 && (
                <div className="mt-6 pt-6 border-t border-sky-300/30">
                  <h4 className="text-xl font-bold mb-3 text-sky-200">Найденные заметки:</h4>
                  <ul className="space-y-2">
                    {documents.map((doc, index) => (
                      <li key={index} className="bg-sky-800/50 p-3 rounded-md text-sm cursor-pointer hover:bg-sky-700/50 transition-colors" onClick={() => setSelectedDocument(doc)}>
                        <p className="font-mono text-sky-300">{doc.file_path}</p>
                        <p className="text-sky-400">Релевантность: {Math.round(doc.similarity * 100)} из 100</p>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </motion.div>
          )}
        </div>

        {/* Инфо-блоки (скрываются при поиске) */}
        {!loading && !result && !error && (
          <>
            <motion.div
              className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-6xl mb-20"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 1 }}
            >
              {[
                { title: "Семантический поиск", description: "Находите информацию по смыслу, а не по ключевым словам. Наша система понимает контекст ваших запросов.", icon: <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>, color: "from-sky-500/20 to-blue-500/20", border: "border-sky-400/30"},
                { title: "ИИ-генерация ответов", description: "Получайте развернутые ответы на основе ваших заметок. Система анализирует контекст и формирует точные ответы.", icon: <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>, color: "from-emerald-500/20 to-green-500/20", border: "border-emerald-400/30"},
                { title: "Синхронизация", description: "Автоматическая синхронизация с Google Drive. Ваши заметки всегда актуальны и доступны в системе поиска.", icon: <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>, color: "from-violet-500/20 to-purple-500/20", border: "border-violet-400/30"}
              ].map((feature, index) => (
                <motion.div
                  key={index}
                  className={`bg-gradient-to-br ${feature.color} backdrop-blur-lg p-8 rounded-2xl ${feature.border} hover:shadow-2xl transition-all duration-300`}
                  whileHover={{ y: -10 }}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 1.2 + index * 0.1 }}
                >
                  <div className="mb-6 flex justify-center"><div className={`p-4 rounded-2xl bg-gradient-to-r ${feature.color.replace('20', '40')} shadow-lg`}>{feature.icon}</div></div>
                  <h3 className="text-2xl font-bold text-white mb-4 text-center">{feature.title}</h3>
                  <p className="text-sky-200 text-center text-lg">{feature.description}</p>
                </motion.div>
              ))}
            </motion.div>
            {/* Статистика */}
            <motion.div
              className="w-full max-w-4xl mb-20"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 1.5 }}
            >
              <div className="bg-sky-900/40 backdrop-blur-lg rounded-2xl p-8 border border-sky-300/20">
                <div className="flex flex-col md:flex-row justify-between items-center">
                  <div className="flex items-center mb-6 md:mb-0">
                    <div className="bg-gradient-to-r from-sky-500/20 to-blue-500/20 p-5 rounded-2xl mr-6 shadow-lg"><svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-sky-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg></div>
                    <div>
                      <p className="text-sky-300 text-lg">Загружено заметок</p>
                      <motion.p className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-sky-300 to-blue-300" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1, delay: 1.7 }}>276</motion.p>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <div className="bg-gradient-to-r from-emerald-500/20 to-green-500/20 p-5 rounded-2xl mr-6 shadow-lg"><svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-emerald-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg></div>
                    <div>
                      <p className="text-sky-300 text-lg">Технология</p>
                      <p className="text-3xl font-bold text-white">Google Gemini</p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </div>

      {/* Футер */}
      <footer className="relative z-10 text-center py-12 text-sky-300 border-t border-sky-300/20">
        <div className="max-w-6xl mx-auto">
          <motion.p 
            className="text-lg"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 2.5 }}
          >
            © 2025 Интеллектуальный поиск по заметкам. Создано <a href="https://t.me/brozaurus" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">@brozaurus</a>
          </motion.p>
        </div>
      </footer>

      {/* Модальное окно */}
      {selectedDocument && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedDocument(null)}
        >
          <motion.div
            initial={{ scale: 0.9, y: 20 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.9, y: 20 }}
            className="bg-sky-900/80 border border-sky-300/30 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-8 shadow-2xl relative"
            onClick={(e) => e.stopPropagation()} // Предотвращаем закрытие по клику внутри окна
          >
            <button 
              onClick={() => setSelectedDocument(null)} 
              className="absolute top-4 right-4 text-sky-300 hover:text-white transition-colors p-2 rounded-full bg-sky-800/50 hover:bg-sky-700/50"
              aria-label="Закрыть"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <h2 className="text-2xl font-bold mb-4 text-sky-200 break-words">{selectedDocument.file_path}</h2>
            <div className="prose prose-invert prose-p:text-sky-200 prose-headings:text-sky-100 prose-a:text-blue-400 hover:prose-a:text-blue-300 prose-strong:text-sky-100 prose-code:text-emerald-300 prose-pre:bg-sky-800/50 prose-blockquote:border-sky-400 prose-blockquote:text-sky-300 max-w-none">
              <ReactMarkdown>{selectedDocument.content}</ReactMarkdown>
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
};

export default HomePage;
