import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-light flex items-center justify-center text-center px-4">
      <div>
        <h1 className="text-8xl font-bold text-primary mb-4">404</h1>
        <div className="w-16 h-1 bg-accent mx-auto mb-6" />
        <h2 className="text-2xl font-bold text-text-main mb-3">Page Not Found</h2>
        <p className="text-gray-500 mb-8">Sorry, we could not find what you were looking for.</p>
        <Link
          href="/"
          className="px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-blue-800 transition"
        >
          Go Back Home
        </Link>
      </div>
    </div>
  );
}
