// ============================================================
// PAGINATED RESPONSE WRAPPER
// ============================================================
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// ============================================================
// HOME
// ============================================================
export interface HomeBanner {
  id: number;
  title: string | null;
  subtitle: string | null;
  image: string;
  button_text: string | null;
  button_link: string | null;
  is_active: boolean;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface ChurchInfo {
  id: number;
  church_name: string;
  tagline: string;
  welcome_message: string;
  full_about: string;
  address: string;
  phone: string;
  email: string;
  mission_statement: string;
  vision_statement: string;
  core_values: string;
  service_times_text: string;
  youtube_channel_url: string | null;
  facebook_url: string | null;
  instagram_url: string | null;
  twitter_url: string | null;
  tiktok_url: string | null;
  whatsapp_url: string | null;
  updated_at: string;
}

export interface HeadPastor {
  id: number;
  name: string;
  title: string;
  full_bio: string;
  image: string;
  email: string | null;
  phone: string | null;
  whatsapp_url: string | null;
  instagram: string | null;
  tiktok: string | null;
  updated_at: string;
}

// ============================================================
// ABOUT
// ============================================================
export interface ServiceTime {
  id: number;
  day: string;
  time: string;
  service_type: string;
  branch: number;
  branch_name: string;
  additional_info: string;
  is_active: boolean;
}

export interface Leader {
  id: number;
  full_name: string;
  position: string;
  biography: string;
  profile_picture: string;
  email: string | null;
  phone: string | null;
  is_featured_on_home: boolean;
  order: number;
  created_at: string;
}

export interface PhotoGallery {
  id: number;
  title: string;
  image: string;
  caption: string;
  category: string;
  uploaded_at: string;
}

// ============================================================
// SERMONS
// ============================================================
export interface Sermon {
  id: number;
  title: string;
  description: string;
  speaker: string;
  date: string;
  video_url: string;
  custom_thumbnail: string | null;
  scripture_reference: string;
  series: string;
  duration: string;
  is_published: boolean;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

// ============================================================
// EVENTS
// ============================================================
export interface Event {
  id: number;
  title: string;
  description: string;
  date: string;
  location: string;
  branch: number | null;
  branch_name: string | null;
  image: string | null;
  category: string;
  registration_link: string | null;
  contact_person: string;
  is_active: boolean;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

// ============================================================
// BRANCHES
// ============================================================
export interface Branch {
  id: number;
  name: string;
  location: string;
  phone: string;
  email: string;
  pastor_in_charge: string;
  service_time: string;
  image: string | null;
  google_maps_url: string | null;
  is_main_branch: boolean;
  service_times: ServiceTime[];
  events_count: number;
  created_at: string;
  updated_at: string;
}

// ============================================================
// GIVING
// ============================================================
export interface GivingImage {
  id: number;
  image: string;
  caption: string;
  order: number;
  created_at: string;
}

export interface GivingInfo {
  id: number;
  flutterwave_link: string;
  title: string;
  instructions: string;
  why_give_message: string;
  images: GivingImage[];
  updated_at: string;
}

// ============================================================
// CONTACT
// ============================================================
export interface ContactMessage {
  id?: number;
  name: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
  is_read?: boolean;
  submitted_at?: string;
}

// ============================================================
// TESTIMONIES
// ============================================================
export interface Testimony {
  id: number;
  name: string;
  testimony_text: string;
  location: string;
  image: string | null;
  show_on_carousel: boolean;
  is_approved: boolean;
  category: string;
  order: number;
  source_message: number | null;
  source_message_name: string | null;
  created_at: string;
  updated_at: string;
}

// ============================================================
// STORE
// ============================================================
export interface Book {
  id: number;
  name: string;
  price: string;
  image: string | null;
  description: string;
  whatsapp_link: string | null;
  email: string | null;
  amazon: string | null;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

export interface Merchandise {
  id: number;
  name: string;
  price: string;
  image: string | null;
  description: string;
  whatsapp_link: string | null;
  jiji_link: string | null;
  amazon_link: string | null;
  email: string | null;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

export interface ExchangeRate {
  id: number;
  currency_code: string;
  currency_name: string;
  rate: string;
  last_updated: string;
}

// Contact form subject choices
export const SUBJECT_CHOICES = [
  "General Inquiry",
  "Prayer Request",
  "Event Information",
  "Service Information",
  "Counseling Request",
  "Partnership",
  "Feedback",
  "Volunteer",
  "Media Request",
  "Other",
] as const;

export type SubjectChoice = (typeof SUBJECT_CHOICES)[number];
