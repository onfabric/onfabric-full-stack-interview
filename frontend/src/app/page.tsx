import { backend } from "@/apis";
import { type User } from "@/types";
import { getApiKeys } from "./actions";
import Dashboard from "@/components/dashboard";

export default async function Home() {
  const [user, keys] = await Promise.all([
    backend.get<User>("/user").then((res) => res.data),
    getApiKeys(),
  ]);

  if (keys === null) {
    return <>error...</>;
  }

  return (
    <div className="grid grid-rows-[auto_1fr_auto] min-h-screen p-8 gap-8">
      <header className="flex justify-between items-center border-b-[1px] pb-2">
        <h1 className="text-2xl font-bold">API Dashboard</h1>
        <div className="flex items-center justify-end gap-2">
          <span className=" rounded-full text-sm text-gray-800">
            {user.email}
          </span>
        </div>
      </header>

      <main className="grid grid-cols-1 gap-2">
        <Dashboard initialKeys={keys} />
      </main>
      <footer className="flex justify-center gap-6 py-8 text-sm text-gray-500">
        <span>© 2024 API Dashboard</span>
      </footer>
    </div>
  );
}
