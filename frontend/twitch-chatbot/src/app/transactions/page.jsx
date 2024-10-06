import react from "react";
import sqlite3 from 'sqlite3'
import { open } from "sqlite";

async function getDataFromDatabase() {
  const db = await open({
    filename: '../../database.db',
    driver: sqlite3.Database
  })

  const data = await db.all(`
    SELECT 
      transactions.id AS transaction_id,
      transactions.userID AS user_id,
      transactions.date AS transaction_date,
      transactions.points AS transaction_points,
      chatters.username AS username,
      commands.name AS action_name
    FROM 
      transactions
      INNER JOIN chatters ON chatters.id = transactions.userID
      INNER JOIN commands ON commands.id = transactions.action
  `)
  console.log(data)

  await db.close()

  return data
}

export default async function Transactions() {
  const data = await getDataFromDatabase()

  return (
    <main className="min-h-screen py-10 flex flex-col">
      <h1 className="text-5xl font-semibold text-center uppercase">Chatters</h1>
      <p className="text-xs text-stone-400 text-center uppercase tracking-wider">All the controls for cresentsbot, all in one place.</p>

      <table className="m-32 bg-stone-900 rounded-md">
        <thead>
          <tr>
            <td>ID</td>
            <td>User ID</td>
            <td>Date</td>
            <td>Chatter Username</td>
            <td>Action Name</td>
            <td>Points</td>
          </tr>
        </thead>
        <tbody>
          {
            data.map(({ transaction_id, user_id, transaction_date, transaction_points, username, action_name }) => (
              <tr key={transaction_id} className="py-2">
                <td>{transaction_id}</td>
                <td>{user_id}</td>
                <td>{transaction_date}</td>
                <td>{username}</td>
                <td>{action_name}</td>
                <td>{transaction_points}</td>
              </tr>
            ))
          }
        </tbody>
      </table>
    </main>
  );
}
