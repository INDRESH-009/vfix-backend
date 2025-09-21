export default function Home() {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="card">
        <h2 className="text-xl font-semibold mb-2">Welcome</h2>
        <p>File a new report, track your issues, and see what’s happening nearby.</p>
      </div>
      <div className="card">
        <h3 className="font-semibold mb-2">Quick links</h3>
        <ul className="list-disc pl-5">
          <li><a href="/report" className="text-blue-600">Report an issue</a></li>
          <li><a href="/issues" className="text-blue-600">My issues</a></li>
          <li><a href="/map" className="text-blue-600">Public map</a></li>
        </ul>
      </div>
    </div>
  );
}
