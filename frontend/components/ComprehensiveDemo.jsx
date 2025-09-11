import { Button } from "@/components/ui/button";
import { 
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";

// Comprehensive demo of shadcn/ui components
export default function ComprehensiveDemo() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
        Комплексная демонстрация shadcn/ui компонентов
      </h1>
      
      <div className="w-full max-w-md space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Форма входа</CardTitle>
            <CardDescription>Введите ваши учетные данные</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">Email</label>
              <Input id="email" type="email" placeholder="your@email.com" />
            </div>
            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">Пароль</label>
              <Input id="password" type="password" placeholder="••••••••" />
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button variant="outline">Отмена</Button>
            <Button>Войти</Button>
          </CardFooter>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Дополнительные действия</CardTitle>
            <CardDescription>Другие доступные опции</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <Button variant="secondary" className="w-full">Зарегистрироваться</Button>
            <Button variant="ghost" className="w-full">Забыли пароль?</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}