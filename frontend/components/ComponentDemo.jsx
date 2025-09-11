import { Button } from "@/components/ui/button";
import { 
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter
} from "@/components/ui/card";

// Example of how to use the Button and Card components in a React component
export default function ComponentDemo() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
        Демонстрация shadcn/ui компонентов
      </h1>
      
      <div className="w-full max-w-md">
        <Card>
          <CardHeader>
            <CardTitle>Карточка</CardTitle>
            <CardDescription>Это пример карточки из shadcn/ui</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700">
              Здесь может быть любой контент, который вы хотите отобразить в карточке.
            </p>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button variant="outline">Отмена</Button>
            <Button>Подтвердить</Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}