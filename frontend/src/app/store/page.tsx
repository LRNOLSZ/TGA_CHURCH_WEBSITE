"use client";

import { useState } from "react";
import Image from "next/image";
import { ShoppingBag, MessageCircle, ExternalLink, BookOpen } from "lucide-react";
import { useBooks, useMerchandise, useExchangeRates } from "@/hooks/useStore";
import { getImageUrl } from "@/lib/utils";
import { Book, Merchandise } from "@/types";
import SectionHeader from "@/components/ui/SectionHeader";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

type Tab = "all" | "books" | "merchandise";

export default function StorePage() {
  const [tab, setTab] = useState<Tab>("all");
  const [currency, setCurrency] = useState("USD");

  const { data: books, isLoading: loadingBooks } = useBooks();
  const { data: merch, isLoading: loadingMerch } = useMerchandise();
  const { data: rates } = useExchangeRates();

  const selectedRate = rates?.find((r) => r.currency_code === currency);

  function convertPrice(priceUsd: string): string {
    const num = parseFloat(priceUsd);
    if (!selectedRate || currency === "USD") return `$${num.toFixed(2)}`;
    const converted = num * parseFloat(selectedRate.rate);
    return `${currency} ${converted.toFixed(2)}`;
  }

  const isLoading = loadingBooks || loadingMerch;

  const showBooks = tab === "all" || tab === "books";
  const showMerch = tab === "all" || tab === "merchandise";

  return (
    <div className="bg-light min-h-screen">
      <div className="bg-primary py-16 text-center">
        <SectionHeader title="Church Store" subtitle="Books, merchandise, and more" light />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center mb-10">
          {/* Tabs */}
          <div className="flex gap-2 bg-white rounded-xl p-1 shadow-sm">
            {(["all", "books", "merchandise"] as Tab[]).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-5 py-2 rounded-lg text-sm font-medium transition-colors capitalize ${
                  tab === t ? "bg-primary text-white" : "text-gray-600 hover:text-primary"
                }`}
              >
                {t}
              </button>
            ))}
          </div>

          {/* Currency */}
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600 font-medium">Currency:</span>
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary bg-white"
            >
              <option value="USD">USD</option>
              {rates?.map((r) => (
                <option key={r.currency_code} value={r.currency_code}>
                  {r.currency_code} — {r.currency_name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {isLoading ? (
          <LoadingSpinner />
        ) : (
          <div className="space-y-12">
            {/* Books */}
            {showBooks && books && books.length > 0 && (
              <div>
                <div className="flex items-center gap-2 mb-6">
                  <BookOpen className="text-primary" size={20} />
                  <h2 className="text-xl font-bold text-primary">Books</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {books.filter((b) => b.is_available).map((book) => (
                    <BookCard key={book.id} book={book} price={convertPrice(book.price)} />
                  ))}
                </div>
              </div>
            )}

            {/* Merchandise */}
            {showMerch && merch && merch.length > 0 && (
              <div>
                <div className="flex items-center gap-2 mb-6">
                  <ShoppingBag className="text-primary" size={20} />
                  <h2 className="text-xl font-bold text-primary">Merchandise</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {merch.filter((m) => m.is_available).map((item) => (
                    <MerchCard key={item.id} item={item} price={convertPrice(item.price)} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function BookCard({ book, price }: { book: Book; price: string }) {
  return (
    <div className="bg-white rounded-2xl shadow-md overflow-hidden group">
      <div className="relative h-52 bg-gray-100">
        <Image src={getImageUrl(book.image)} alt={book.name} fill className="object-cover group-hover:scale-105 transition-transform duration-300" />
      </div>
      <div className="p-5">
        <h3 className="font-bold text-text-main mb-1">{book.name}</h3>
        <p className="text-accent font-bold text-lg mb-2">{price}</p>
        <p className="text-gray-500 text-sm mb-4 line-clamp-2">{book.description}</p>
        <div className="flex gap-2 flex-wrap">
          {book.whatsapp_link && (
            <a href={book.whatsapp_link} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-1 px-3 py-1.5 bg-green-500 text-white text-xs font-medium rounded-lg hover:bg-green-600 transition">
              <MessageCircle size={12} /> WhatsApp
            </a>
          )}
          {book.amazon && (
            <a href={book.amazon} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-1 px-3 py-1.5 bg-amber-500 text-white text-xs font-medium rounded-lg hover:bg-amber-600 transition">
              <ExternalLink size={12} /> Amazon
            </a>
          )}
        </div>
      </div>
    </div>
  );
}

function MerchCard({ item, price }: { item: Merchandise; price: string }) {
  return (
    <div className="bg-white rounded-2xl shadow-md overflow-hidden group">
      <div className="relative h-52 bg-gray-100">
        <Image src={getImageUrl(item.image)} alt={item.name} fill className="object-cover group-hover:scale-105 transition-transform duration-300" />
      </div>
      <div className="p-5">
        <h3 className="font-bold text-text-main mb-1">{item.name}</h3>
        <p className="text-accent font-bold text-lg mb-2">{price}</p>
        <p className="text-gray-500 text-sm mb-4 line-clamp-2">{item.description}</p>
        <div className="flex gap-2 flex-wrap">
          {item.whatsapp_link && (
            <a href={item.whatsapp_link} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-1 px-3 py-1.5 bg-green-500 text-white text-xs font-medium rounded-lg hover:bg-green-600 transition">
              <MessageCircle size={12} /> WhatsApp
            </a>
          )}
          {item.jiji_link && (
            <a href={item.jiji_link} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-1 px-3 py-1.5 bg-blue-500 text-white text-xs font-medium rounded-lg hover:bg-blue-600 transition">
              <ExternalLink size={12} /> Jiji
            </a>
          )}
          {item.amazon_link && (
            <a href={item.amazon_link} target="_blank" rel="noopener noreferrer"
              className="flex items-center gap-1 px-3 py-1.5 bg-amber-500 text-white text-xs font-medium rounded-lg hover:bg-amber-600 transition">
              <ExternalLink size={12} /> Amazon
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
