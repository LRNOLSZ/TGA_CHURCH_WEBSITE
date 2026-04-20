import Image from "next/image";
import Link from "next/link";
import { Play, Calendar, User, BookOpen } from "lucide-react";
import { Sermon } from "@/types";
import { formatDate, getYouTubeThumbnail, getImageUrl } from "@/lib/utils";

export default function SermonCard({ sermon }: { sermon: Sermon }) {
  const thumbnail = sermon.custom_thumbnail
    ? getImageUrl(sermon.custom_thumbnail)
    : getYouTubeThumbnail(sermon.video_url);

  return (
    <div className="bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition-shadow group">
      {/* Thumbnail */}
      <div className="relative h-48 bg-gray-100">
        <Image src={thumbnail} alt={sermon.title} fill className="object-cover" />
        <div className="absolute inset-0 bg-dark/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
          <div className="w-14 h-14 rounded-full bg-accent flex items-center justify-center">
            <Play size={24} className="text-white ml-1" />
          </div>
        </div>
        {sermon.series && (
          <div className="absolute top-3 left-3 bg-primary text-white text-xs font-semibold px-2 py-1 rounded">
            {sermon.series}
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-5">
        <h3 className="font-bold text-text-main text-lg mb-3 line-clamp-2 group-hover:text-primary transition-colors">
          {sermon.title}
        </h3>

        <div className="space-y-1.5 mb-4 text-sm text-gray-500">
          <div className="flex items-center gap-2">
            <User size={13} className="text-accent" />
            <span>{sermon.speaker}</span>
          </div>
          <div className="flex items-center gap-2">
            <Calendar size={13} className="text-accent" />
            <span>{formatDate(sermon.date)}</span>
          </div>
          {sermon.scripture_reference && (
            <div className="flex items-center gap-2">
              <BookOpen size={13} className="text-accent" />
              <span className="italic">{sermon.scripture_reference}</span>
            </div>
          )}
        </div>

        <Link
          href={`/sermons/${sermon.id}`}
          className="flex items-center justify-center gap-2 w-full px-4 py-2 bg-primary text-white font-medium rounded-lg text-sm hover:bg-blue-800 transition-colors"
        >
          <Play size={14} /> Watch Sermon
        </Link>
      </div>
    </div>
  );
}
