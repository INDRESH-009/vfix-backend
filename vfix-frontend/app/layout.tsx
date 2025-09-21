import "./globals.css";
import Link from "next/link";
import { Toaster } from "react-hot-toast";

export const metadata = { title: "VFix Citizen", description: "Report civic issues" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">
        <header className="border-b bg-white">
          <nav className="container flex items-center justify-between py-3">
            <Link href="/" className="font-bold">VFix</Link>
            <div className="flex gap-4 text-sm">
              <Link href="/report">Report Issue</Link>
              <Link href="/issues">My Issues</Link>
              <Link href="/map">Nearby</Link>
              <Link href="/login">Login</Link>
            </div>
          </nav>
        </header>
        <main className="container py-6">{children}</main>
        <Toaster />
      </body>
    </html>
  );
}
