// === Base types from admin (shared) ===

export interface OnboardingItem {
  key: string;
  label: string;
  completed: boolean;
  note?: string;
}

export interface StorySlot {
  id: string;
  day: number;
  date: string;
  slot: 1 | 2 | 3;
  week: number;
  theme: string;
  contentType: 'A' | 'P' | 'R';
  status: 'pending' | 'generated' | 'approved' | 'rejected' | 'published' | 'failed';
  templateId?: number;
  previewUrl?: string;
  caption?: string;
  // Portal extensions
  editedCaption?: string;
  ownerPhotoUrl?: string;
  swappedTemplateId?: number;
  approvedAt?: string;
  rejectedAt?: string;
  rejectionReason?: string;
}

export interface ReelItem {
  id: string;
  week: number;
  theme: string;
  status: 'pending' | 'scripted' | 'generated' | 'approved' | 'rejected' | 'published' | 'failed';
  duration: number;
  cost: number;
  // Portal extensions
  scriptText?: string;
  scriptApproved?: boolean;
  videoApproved?: boolean;
  revisionRequest?: string;
  approvedAt?: string;
  rejectedAt?: string;
}

export interface SeoPost {
  id: string;
  title: string;
  status: 'pending' | 'draft' | 'approved' | 'rejected' | 'published';
  publishDate?: string;
  excerpt?: string;
  editedTitle?: string;
  editedExcerpt?: string;
  approvedAt?: string;
  rejectedAt?: string;
}

export interface SeoChannel {
  channel: 'blog' | 'twitter' | 'reddit' | 'quora' | 'gbp';
  label: string;
  postsPlanned: number;
  postsPublished: number;
  status: 'active' | 'paused' | 'pending';
  // Portal extension
  posts?: SeoPost[];
}

export interface ClinicCost {
  stories: number;
  reels: number;
  seo: number;
  total: number;
  month: string;
}

export interface AutoApproveRules {
  stories: boolean;
  reels: boolean;
  seo: boolean;
}

export interface NotificationPrefs {
  email: boolean;
  whatsapp: boolean;
  weeklyDigest: boolean;
}

export interface ClinicPortalSettings {
  autoApproveRules: AutoApproveRules;
  toneOfVoice: string;
  notificationPrefs: NotificationPrefs;
  brandColors: { primary: string; accent: string };
  photoVault: string[];
}

// === AI Visibility / GEO types ===

export interface AiPlatformCoverage {
  platform: 'google_aio' | 'chatgpt' | 'perplexity' | 'gemini';
  mentioned: 'yes' | 'partial' | 'no';
  sentiment: 'positive' | 'neutral' | 'negative' | null;
  sampleQueries: string[];
}

export interface AiQueryPerformance {
  query: string;
  platforms: Record<string, boolean>; // platform key → mentioned
  competitorsMentioned: string[];
  trend: 'up' | 'down' | 'stable' | 'new';
}

export interface AiOptimizationCheck {
  key: string;
  label: string;
  completed: boolean;
  priority: 'high' | 'medium' | 'low';
  impact: string;
}

export interface AiCompetitor {
  name: string;
  aiScore: number;
  platformsCovered: number;
  shareOfVoice: number;
}

export interface AiVisibilityData {
  overallScore: number;
  scoreTrend: 'up' | 'down' | 'stable';
  scoreLastWeek: number;
  platforms: AiPlatformCoverage[];
  queries: AiQueryPerformance[];
  optimizationChecklist: AiOptimizationCheck[];
  competitors: AiCompetitor[];
  lastUpdated: string;
}

export interface ClinicDetail {
  id: number;
  name: string;
  city: string;
  address: string;
  phone: string;
  website: string;
  segment: number;
  segmentName: string;
  rating: number;
  reviewCount: number;
  siteScore: number;
  colors: { primary: string; accent: string };
  onboarding: OnboardingItem[];
  stories: StorySlot[];
  reels: ReelItem[];
  seoChannels: SeoChannel[];
  costs: ClinicCost[];
  // Portal extensions
  portalSettings?: ClinicPortalSettings;
  aiVisibility?: AiVisibilityData;
}

export interface TokenMap {
  [token: string]: number;
}

export interface ActivityItem {
  id: string;
  action: string;
  detail: string;
  timestamp: string;
  pipeline: 'stories' | 'reels' | 'seo' | 'system';
}

// Template info for template picker
export interface TemplateInfo {
  id: number;
  name: string;
  category: string;
  previewPath: string;
}

// Calendar item for unified calendar view
export interface CalendarItem {
  id: string;
  date: string;
  type: 'story' | 'reel' | 'seo';
  title: string;
  status: string;
  slot?: number;
  channel?: string;
}
