import { Button } from "@/components/ui/button";

// Example of how to use the Button component in a React component
export default function SearchExample() {
  const handleSearch = () => {
    console.log("Search initiated");
    // Add your search logic here
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
        Интеллектуальный поиск по заметкам
      </h1>
      <div className="w-full max-w-md">
        <div className="flex mb-4">
          <input
            type="text"
            placeholder="Введите ваш запрос..."
            className="flex-grow px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <Button onClick={handleSearch} variant="default">
            Искать
          </Button>
        </div>
      </div>
    </div>
  );
}