import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Senatordle",
  description: "Can you guess whether a US Senator is Republican or Democrat based solely on their portrait?",
  openGraph: {
    title: "Senatordle",
    description: "Can you guess whether a US Senator is Republican or Democrat based solely on their portrait?",
    images: [
      {
        url: "https://senatordle.com/senatordle.png",
        alt: "Senatordle",
      },
    ],
    type: "website",
  },
  twitter: {
    card: "summary",
    title: "Senatordle",
    description: "Can you guess whether a US Senator is Republican or Democrat based solely on their portrait?",
    images: ["https://senatordle.com/senatordle.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
