import react from "react";
import sqlite3 from 'sqlite3'
import { open } from "sqlite";

async function getDataFromDatabase() {
  const db = await open({
    filename: '../../database.db',
    driver: sqlite3.Database
  })

  const data = await db.all(`
    SELECT * FROM commands
  `)
  console.log(data)

  await db.close()

  return data
}

export default async function Transactions() {
  const data = await getDataFromDatabase()

  return (
    <main className="min-h-screen py-10 flex flex-col">
      <h1 className="text-5xl font-semibold text-center uppercase">Commands</h1>
      <p className="text-xs text-stone-400 text-center uppercase tracking-wider">All the controls for cresentsbot, all in one place.</p>

      <div className="w-[100%] flex flex-col gap-2 items-center my-20">
        <div className="p-2 bg-[#1c1917] w-[75%] rounded-md grid grid-cols-5">
          <h1>ID</h1>
          <h1>Name</h1>
          <h1>Points</h1>
          <h1>Action</h1>
          <h1>Inputs</h1>
        </div>

        {
          data.map(({ id, name, points, action, params }) => (
            <div key={id} className="p-2 bg-stone-900 w-[75%] rounded-md grid grid-cols-5">
              <h1>{id}</h1>
              <h1>{name}</h1>
              <h1>{points}</h1>
              <h1>{action}</h1>
              <h1>{params}</h1>
            </div>
          ))
        }
      </div>
      
      <h1 className="text-3xl font-medium text-center uppercase">Add Command</h1>
      <form action="" className="w-full">
        <input type="text" placeholder="Command Name" />
      </form>
    </main>
  );
}
