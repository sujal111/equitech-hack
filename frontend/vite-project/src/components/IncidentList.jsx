// export default function IncidentList({ incidents }) {
//     return (
//       <div>
//         <h2>Incidents</h2>
//         <ul>
//           {incidents.map((inc) => (
//             <li key={inc.id}>
//               {inc.title} - {inc.status} - {inc.message}
//             </li>
//           ))}
//         </ul>
//       </div>
//     );
//   }
  



export default function IncidentList({ incidents }) {
  return (
    <div className="list">
      <h2>Incidents</h2>
      {incidents.length === 0 ? (
        <p className="empty">No incidents yet</p>
      ) : (
        <ul>
          {incidents.map((inc) => (
            <li key={inc.id} className="incident-card">
              <h3>{inc.title}</h3>
              <p>{inc.message}</p>
              <span className={`badge ${inc.severity.toLowerCase()}`}>
                {inc.severity}
              </span>
              <p className="status">Status: {inc.status}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
