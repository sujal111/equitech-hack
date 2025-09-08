// // import { useState } from 'react'
// // import reactLogo from './assets/react.svg'
// // import viteLogo from '/vite.svg'
// // import './App.css'

// // function App() {
// //   const [count, setCount] = useState(0)

// //   return (
// //     <>
// //       <div>
// //         <a href="https://vite.dev" target="_blank">
// //           <img src={viteLogo} className="logo" alt="Vite logo" />
// //         </a>
// //         <a href="https://react.dev" target="_blank">
// //           <img src={reactLogo} className="logo react" alt="React logo" />
// //         </a>
// //       </div>
// //       <h1>Vite + React</h1>
// //       <div className="card">
// //         <button onClick={() => setCount((count) => count + 1)}>
// //           count is {count}
// //         </button>
// //         <p>
// //           Edit <code>src/App.jsx</code> and save to test HMR
// //         </p>
// //       </div>
// //       <p className="read-the-docs">
// //         Click on the Vite and React logos to learn more
// //       </p>
// //     </>
// //   )
// // }

// // export default App



// import { useState } from "react";
// import IncidentForm from "./components/IncidentForm";
// import IncidentList from "./components/IncidentList";

// function App() {
//   const [incidents, setIncidents] = useState([]);

//   const addIncident = (incident) => {
//     setIncidents([...incidents, incident]);
//   };

//   return (
//     <div className="p-6">
//       <h1>🚨 Incident AI POC</h1>
//       <IncidentForm onNewIncident={addIncident} />
//       <IncidentList incidents={incidents} />
//     </div>
//   );
// }

// export default App;




import { useState } from "react";
import IncidentForm from "./components/IncidentForm";
import IncidentList from "./components/IncidentList";
import "./App.css";

function App() {
  const [incidents, setIncidents] = useState([]);

  const addIncident = (incident) => {
    setIncidents([...incidents, incident]);
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🚨 Incident AI POC</h1>
      </header>
      <main>
        <IncidentForm onNewIncident={addIncident} />
        <IncidentList incidents={incidents} />
      </main>
    </div>
  );
}

export default App;

