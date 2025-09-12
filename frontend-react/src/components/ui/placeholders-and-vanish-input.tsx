import React, { useEffect, useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "../../utils/cn";

export const PlaceholdersAndVanishInput = ({
  placeholders,
  onChange,
  onSubmit,
  onClear,
  value,
}: {
  placeholders: string[];
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  onClear: () => void;
  value: string;
}) => {
  const [currentPlaceholder, setCurrentPlaceholder] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (!value) {
      interval = setInterval(() => {
        setCurrentPlaceholder((prev) => (prev + 1) % placeholders.length);
      }, 2000);
    }

    return () => clearInterval(interval);
  }, [value, placeholders.length]);

  const handleClearClick = () => {
    if (inputRef.current) {
      inputRef.current.value = "";
      onChange({ target: { value: "" } } as React.ChangeEvent<HTMLInputElement>);
    }
    onClear();
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(e);
  };

  return (
    <div className="relative group w-full">
      <div className="absolute -inset-1 bg-gradient-to-r from-sky-400 to-blue-500 rounded-xl blur opacity-75 group-hover:opacity-100 transition-all duration-300"></div>
      <form
        className={cn(
          "relative flex flex-col sm:flex-row gap-3 rounded-xl overflow-hidden shadow-xl bg-sky-900/50 backdrop-blur-lg border border-sky-300/20",
          value && "justify-start"
        )}
        onSubmit={handleSubmit}
      >
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={onChange}
          placeholder={value ? "" : placeholders[currentPlaceholder]}
          className={cn(
            "flex-grow px-6 py-5 text-sky-100 bg-transparent focus:outline-none border-0 placeholder-sky-300 text-lg",
            value && "placeholder-transparent"
          )}
        />

        {value && (
          <motion.div
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.5 }}
            transition={{ duration: 0.2 }}
            className="flex items-center justify-center pr-3"
          >
            <button
              type="button"
              onClick={handleClearClick}
              className="p-2 rounded-full bg-sky-800/50 hover:bg-sky-700/50 text-sky-300 hover:text-white transition-colors"
              aria-label="Очистить поиск"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </motion.div>
        )}

        <motion.button
          type="submit"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="relative bg-gradient-to-r from-sky-500 to-blue-600 text-white font-bold py-5 px-8 rounded-lg transition-all duration-300 shadow-lg text-lg"
        >
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            Искать
          </div>
        </motion.button>
      </form>
    </div>
  );
};
