"use client";

import { useState } from "react";
import Image from "next/image";
import { ShoppingBag, MessageCircle, ExternalLink, BookOpen } from "lucide-react";
import { useBooks, useMerchandise } from "@/hooks/useStore";
import { getImageUrl } from "@/lib/utils";
import { Book, Merchandise } from "@/types";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import FadeIn from "@/components/ui/FadeIn";

type Tab = "all" | "books" | "merchandise";

export default function StorePage() {
  const [tab, setTab] = useState<Tab>("all");

  const { data: books, isLoading: loadingBooks } = useBooks();
  const { data: merch, isLoading: loadingMerch } = useMerchandise();

  function formatPrice(price: string): string {
    const num = parseFloat(price);
    if (num === 0) return "";
    return `₵${num.toFixed(2)}`;
  }

  const isLoading = loadingBooks || loadingMerch;

  const showBooks = tab === "all" || tab === "books";
  const showMerch = tab === "all" || tab === "merchandise";

  return (
    <div className="bg-bg min-h-screen">
      <div className="bg-navy py-16 text-center">
        <SectionHeader title="Church Store" subtitle="Books, merchandise, and more" light />
      </div>

      <FadeIn>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex gap-2 bg-white rounded-xl p-1 shadow-sm mb-10">
            {(["all", "books", "merchandise"] as Tab[]).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-5 py-2 rounded-lg text-sm font-medium transition-colors capitalize ${
                  tab === t ? "bg-navy text-white" : "text-gray-600 hover:text-primary"
                }`}
              >
                {t}
              </button>
            ))}
          </div>
          {isLoading ? (
            <LoadingSpinner />
          ) : !books?.filter((b) => b.is_available).length && !merch?.filter((m) => m.is_available).length ? (
            <div className="text-center py-24">
              <ShoppingBag className="mx-auto text-gray-300 mb-4" size={48} />
              <p className="text-gray-500 font-medium text-lg">No products available yet.</p>
              <p className="text-gray-400 text-sm mt-1">Check back soon!</p>
            </div>
          ) : (
            <div className="space-y-12">
              {showBooks && books && books.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-6">
                    <BookOpen className="text-primary" size={20} />
                    <h2 className="text-xl font-bold text-primary">Books</h2>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {books.filter((b) => b.is_available).map((book) => (
                      <BookCard key={book.id} book={book} price={formatPrice(book.price)} />
                    ))}
                  </div>
                </div>
              )}
              {showMerch && merch && merch.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-6">
                    <ShoppingBag className="text-primary" size={20} />
                    <h2 className="text-xl font-bold text-primary">Merchandise</h2>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {merch.filter((m) => m.is_available).map((item) => (
                      <MerchCard key={item.id} item={item} price={formatPrice(item.price)} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </FadeIn>
    </div>
  );
}

function BookCard({ book, price }: { book: Book; price: string }) {
  return (
    <div className="overflow-hidden group">
      <div className="relative h-52 bg-gray-100">
        <Image src={getImageUrl(book.image)} alt={book.name} fill className="object-cover group-hover:scale-105 transition-transform duration-300" />
      </div>
      <div className="p-5">
        <h3 className="font-bold text-text-main mb-1">{book.name}</h3>
        {price && <p className="text-accent font-bold text-lg mb-2">{price}</p>}
        <p className="text-gray-500 text-sm mb-4 line-clamp-2">{book.description}</p>
        <div className="flex gap-2 flex-wrap">
          {book.whatsapp_link && (
            <a href={book.whatsapp_link} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-1.5 px-3 py-1.5 bg-green-500 text-white text-xs font-medium rounded-lg hover:bg-green-600 transition">
              <MessageCircle size={13} /> Order on WhatsApp
            </a>
          )}
          {book.amazon && (
            <a href={book.amazon} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 text-white text-xs font-medium rounded-lg hover:bg-amber-600 transition">
              <ExternalLink size={13} /> Buy on Amazon
            </a>
          )}
        </div>
      </div>
    </div>
  );
}

function MerchCard({ item, price }: { item: Merchandise; price: string }) {
  const sizes = item.has_sizes && item.available_sizes
    ? item.available_sizes.split(",").map((s) => s.trim()).filter(Boolean)
    : [];

  return (
    <div className="overflow-hidden group">
      <div className="relative h-52 bg-gray-100">
        <Image src={getImageUrl(item.image)} alt={item.name} fill className="object-cover group-hover:scale-105 transition-transform duration-300" />
      </div>
      <div className="p-5">
        <h3 className="font-bold text-text-main mb-1">{item.name}</h3>
        {price && <p className="text-accent font-bold text-lg mb-1">{price}</p>}
        <p className="text-gray-500 text-sm mb-3 line-clamp-2">{item.description}</p>

        {/* Sizes */}
        {sizes.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {sizes.map((size) => (
              <span key={size} className="px-2.5 py-0.5 text-xs font-medium border border-navy/30 text-navy rounded-full">
                {size}
              </span>
            ))}
          </div>
        )}

        {/* Buy buttons */}
        <div className="flex gap-2 flex-wrap">
          {item.whatsapp_link && (
            <a href={item.whatsapp_link} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-1.5 px-3 py-1.5 bg-green-500 text-white text-xs font-medium rounded-lg hover:bg-green-600 transition">
              <MessageCircle size={13} /> Order on WhatsApp
            </a>
          )}
          {item.amazon_link && (
            <a href={item.amazon_link} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-500 text-white text-xs font-medium rounded-lg hover:bg-amber-600 transition">
              <ExternalLink size={13} /> Buy on Amazon
            </a>
          )}
          {item.jiji_link && (
            <a href={item.jiji_link} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-500 text-white text-xs font-medium rounded-lg hover:bg-blue-600 transition">
              <ExternalLink size={13} /> Jiji
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
