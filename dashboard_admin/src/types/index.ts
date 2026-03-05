// === System Status ===
export interface PipelineStatus {
  name: 'stories' | 'reels' | 'seo';
  label: string;
  total: number;
  completed: number;
  inProgress: number;
  failed: number;
  status: 'healthy' | 'warning' | 'critical';
}

export interface BudgetSummary {
  totalBudget: number;
  spent: number;
  projected: number;
  currency: string;
}

export interface Alert {
  id: string;
  level: 'info' | 'warning' | 'error';
  message: string;
  timestamp: string;
  pipeline?: string;
}

export interface ActivityItem {
  id: string;
  action: string;
  detail: string;
  timestamp: string;
  pipeline: 'stories' | 'reels' | 'seo' | 'system';
}

export interface SystemStatus {
  lastUpdated: string;
  pipelines: PipelineStatus[];
  budget: BudgetSummary;
  alerts: Alert[];
  activity: ActivityItem[];
  kpis: {
    totalClinics: number;
    storiesGenerated: number;
    reelsGenerated: number;
    seoPostsPublished: number;
  };
}

// === Clinics ===
export interface ClinicSummary {
  id: number;
  name: string;
  city: string;
  segment: number;
  segmentName: string;
  rating: number;
  reviewCount: number;
  siteScore: number;
  storiesCompleted: number;
  storiesTotal: number;
  reelsCompleted: number;
  reelsTotal: number;
  seoCompleted: number;
  seoTotal: number;
  onboardingPct: number;
}

export interface ClinicIndex {
  lastUpdated: string;
  totalClinics: number;
  clinics: ClinicSummary[];
}

export interface OnboardingItem {
  key: string;
  label: string;
  completed: boolean;
  note?: string;
}

export interface StorySlot {
  day: number;
  date: string;
  slot: 1 | 2 | 3;
  theme: string;
  contentType: 'A' | 'P' | 'R';
  status: 'pending' | 'generated' | 'published' | 'failed';
  templateId?: number;
  previewUrl?: string;
}

export interface ReelItem {
  id: string;
  week: number;
  theme: string;
  status: 'pending' | 'scripted' | 'generated' | 'published' | 'failed';
  duration: number;
  cost: number;
}

export interface SeoChannel {
  channel: 'blog' | 'twitter' | 'reddit' | 'quora' | 'gbp';
  label: string;
  postsPlanned: number;
  postsPublished: number;
  status: 'active' | 'paused' | 'pending';
}

export interface ClinicCost {
  stories: number;
  reels: number;
  seo: number;
  total: number;
  month: string;
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
}

// === Calendar ===
export interface CalendarSlot {
  day: number;
  date: string;
  weekNumber: number;
  theme: string;
  slots: {
    slot: 1 | 2 | 3;
    time: string;
    contentType: 'A' | 'P' | 'R';
    generated: number;
    published: number;
    total: number;
  }[];
}

export interface CalendarData {
  lastUpdated: string;
  startDate: string;
  totalDays: number;
  totalWeeks: number;
  days: CalendarSlot[];
}

// === Templates ===
export interface TemplateInfo {
  id: number;
  name: string;
  category: string;
  usageCount: number;
  assignedClinics: number;
  renderSuccessRate: number;
  lastUsed: string;
  previewPath: string;
}

export interface TemplatesData {
  lastUpdated: string;
  templates: TemplateInfo[];
}

// === Budget ===
export interface MonthlyBudget {
  month: string;
  stories: number;
  reels: number;
  seo: number;
  total: number;
  budget: number;
}

export interface BudgetData {
  lastUpdated: string;
  currency: string;
  monthlyBudget: number;
  currentMonth: MonthlyBudget;
  history: MonthlyBudget[];
  perClinicAvg: {
    stories: number;
    reels: number;
    seo: number;
    total: number;
  };
}
