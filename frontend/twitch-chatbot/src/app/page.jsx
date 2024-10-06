import react from "react";

export default function Home() {
  return (
    <main className="h-screen py-10 flex flex-col justify-center items-center">
      <h1 className="text-5xl font-semibold text-center uppercase">Cresents Chatbot</h1>
      <p className="text-xs text-stone-400 text-center uppercase tracking-wider">All the controls for cresentsbot, all in one place.</p>

      <div className="w-fit sm:w-full flex flex-col sm:flex-row justify-center gap-3 pt-20">
        <a className="link-button" href="/commands">Commands</a>
        <a className="link-button" href="/transactions">All Transactions</a>
      </div>
    </main>
  );
}
