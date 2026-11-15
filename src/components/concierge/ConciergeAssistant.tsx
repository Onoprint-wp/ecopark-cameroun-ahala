// ============================================================================
// ECOPARK CAMEROUN (YAOUNDÉ - AHALA, RN3) - WIDGET CONCIERGE VIRTUEL BILINGUE
// (src/components/concierge/ConciergeAssistant.tsx)
// Accueil conversationnel 24h/24 FR/EN autonome (Vercel Edge, session isolée)
// avec navigation 1 clic et transfert pré-qualifié vers WhatsApp officiel.
// ============================================================================

import React, { useState, useEffect, useRef } from 'react';
import {
  MessageSquareText,
  X,
  Send,
  Sparkles,
  RotateCcw,
  ArrowUpRight,
  PhoneCall,
  Globe,
} from 'lucide-react';
import { useEcoPark } from '../../context/EcoParkContext';
import { dispatchShowcaseNavigation } from '../../utils/ecoRouting';
import { recordMotionOrigin } from '../../utils/ecoMotion';
import {
  CONCIERGE_QUICK_PROMPTS,
  generateConciergeReply,
  getConciergeWelcome,
  type ConciergeLang,
  type ConciergeNavigationAction,
  type ConciergeReply,
} from '../../utils/conciergeEngine';
import {
  getWhatsAppUrl,
  OFFICIAL_PHONE_NUMBERS,
  OUTGOING_WHATSAPP_TEMPLATES,
} from '../../utils/outgoingTemplates';

interface ChatTurn {
  id: string;
  role: 'user' | 'assistant';
  text?: string;
  reply?: ConciergeReply;
  createdAt: string;
}

const SESSION_STORAGE_KEY = 'ecopark_concierge_session_v1';

export const ConciergeAssistant: React.FC = () => {
  const { activeView, setActiveView } = useEcoPark();
  const [isOpen, setIsOpen] = useState(false);
  const [lang, setLang] = useState<ConciergeLang>('fr');
  const [inputValue, setInputValue] = useState('');
  const [turns, setTurns] = useState<ChatTurn[]>(() => {
    if (typeof window === 'undefined') return [];
    try {
      const raw = window.sessionStorage.getItem(SESSION_STORAGE_KEY);
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed.slice(-16) : [];
    } catch {
      return [];
    }
  });

  const launcherRef = useRef<HTMLButtonElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const scrollEndRef = useRef<HTMLDivElement | null>(null);

  // Scission stricte : pas de bulle grand public sur la console d'exploitation métier
  const isOperationalCockpit = activeView === 'ranger';

  useEffect(() => {
    if (typeof window === 'undefined') return;
    try {
      window.sessionStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(turns.slice(-16)));
    } catch {
      // Session storage full or restricted - ignore silently
    }
  }, [turns]);

  useEffect(() => {
    if (!isOpen) return;
    const timer = window.setTimeout(() => {
      scrollEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }, 40);
    return () => window.clearTimeout(timer);
  }, [turns, isOpen]);

  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        setIsOpen(false);
        launcherRef.current?.focus();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  if (isOperationalCockpit) {
    return null;
  }

  const welcome = getConciergeWelcome(lang);
  const quickPrompts = CONCIERGE_QUICK_PROMPTS[lang];

  const submitQuestion = (questionText: string) => {
    const trimmed = questionText.trim();
    if (!trimmed) return;

    const nowTime = new Date().toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit',
    });

    const reply = generateConciergeReply(trimmed, lang);
    if (reply.lang !== lang) {
      setLang(reply.lang);
    }

    const userTurn: ChatTurn = {
      id: `u-${Date.now()}`,
      role: 'user',
      text: trimmed,
      createdAt: nowTime,
    };

    const assistantTurn: ChatTurn = {
      id: `a-${Date.now() + 1}`,
      role: 'assistant',
      reply,
      createdAt: nowTime,
    };

    setTurns((prev) => [...prev.slice(-14), userTurn, assistantTurn]);
    setInputValue('');
  };

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    submitQuestion(inputValue);
  };

  const handleNavAction = (
    action: ConciergeNavigationAction,
    e: React.MouseEvent<HTMLButtonElement>
  ) => {
    recordMotionOrigin(e);
    if (activeView !== action.targetView) {
      setActiveView(action.targetView);
    }
    if (action.showcaseTab || action.anchorId) {
      window.setTimeout(() => {
        dispatchShowcaseNavigation({
          tab: action.showcaseTab,
          anchorId: action.anchorId,
        });
      }, 70);
    }
    setIsOpen(false);
  };

  const handleReset = () => {
    setTurns([]);
    if (typeof window !== 'undefined') {
      try {
        window.sessionStorage.removeItem(SESSION_STORAGE_KEY);
      } catch {
        // ignore
      }
    }
    inputRef.current?.focus();
  };

  const defaultWhatsAppHref = getWhatsAppUrl(
    OFFICIAL_PHONE_NUMBERS.DIRECTION,
    lang === 'en'
      ? 'Hello EcoPark Cameroun, I would like assistance with rates or booking at Ahala.'
      : OUTGOING_WHATSAPP_TEMPLATES.TICKETING_RESERVATION
  );

  return (
    <div className="fixed bottom-4 right-3 sm:bottom-6 sm:right-6 z-40 flex flex-col items-end max-w-[calc(100vw-1.5rem)]">
      {isOpen && (
        <div
          role="dialog"
          aria-modal="false"
          aria-label={welcome.title}
          className="mb-3 w-[calc(100vw-1.5rem)] sm:w-[400px] max-h-[min(620px,calc(100vh-6.5rem))] flex flex-col rounded-2xl bg-[var(--bg-surface)] border-2 border-[#2D6A4F] shadow-2xl overflow-hidden text-[var(--text-primary)]"
        >
          {/* En-tête Concierge avec sélecteur bilingue FR / EN */}
          <div className="bg-[#1B4332] text-white px-4 py-3 border-b border-[#2D6A4F]">
            <div className="flex items-start justify-between gap-2">
              <div className="min-w-0">
                <div className="flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-[#74C69D] shrink-0" />
                  <h2 className="font-sans font-bold text-sm sm:text-base leading-tight truncate">
                    {welcome.title}
                  </h2>
                </div>
                <p className="text-xs text-[#D8F3DC] mt-0.5 leading-snug">
                  {welcome.subtitle}
                </p>
              </div>

              <div className="flex items-center gap-1 shrink-0">
                <button
                  type="button"
                  onClick={() => setLang(lang === 'fr' ? 'en' : 'fr')}
                  aria-label={
                    lang === 'fr'
                      ? 'Passer le Concierge en anglais (EN)'
                      : 'Switch Concierge to French (FR)'
                  }
                  className="min-h-[44px] min-w-[52px] px-2.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/25 text-xs font-bold text-white inline-flex items-center justify-center gap-1 cursor-pointer transition-colors"
                >
                  <Globe className="w-3.5 h-3.5 text-[#74C69D]" />
                  <span>{lang === 'fr' ? 'EN' : 'FR'}</span>
                </button>

                {turns.length > 0 && (
                  <button
                    type="button"
                    onClick={handleReset}
                    aria-label={
                      lang === 'fr'
                        ? 'Réinitialiser la conversation'
                        : 'Reset conversation'
                    }
                    className="min-h-[44px] min-w-[44px] rounded-xl bg-white/10 hover:bg-white/20 text-[#D8F3DC] hover:text-white inline-flex items-center justify-center cursor-pointer transition-colors"
                  >
                    <RotateCcw className="w-4 h-4" />
                  </button>
                )}

                <button
                  type="button"
                  onClick={() => {
                    setIsOpen(false);
                    launcherRef.current?.focus();
                  }}
                  aria-label={
                    lang === 'fr'
                      ? 'Fermer le Concierge Virtuel'
                      : 'Close Virtual Concierge'
                  }
                  className="min-h-[44px] min-w-[44px] rounded-xl bg-white/10 hover:bg-white/20 text-white inline-flex items-center justify-center cursor-pointer transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          {/* Fil de conversation */}
          <div className="flex-1 overflow-y-auto p-3.5 space-y-3 bg-[var(--bg-canvas)] min-h-[220px]">
            {/* Message d'accueil permanent */}
            <div className="p-3 rounded-xl bg-[var(--bg-surface)] border border-[var(--border-default)] text-xs sm:text-sm leading-relaxed text-[var(--text-primary)] shadow-2xs">
              <p>{welcome.greeting}</p>
            </div>

            {/* Suggestions 1 clic */}
            <div className="space-y-1.5">
              <div className="text-[11px] font-semibold uppercase tracking-wider text-[var(--text-muted)] px-0.5">
                {lang === 'fr' ? 'Questions rapides (1 clic)' : 'Quick topics (1 click)'}
              </div>
              <div className="flex flex-wrap gap-1.5">
                {quickPrompts.map((chip) => (
                  <button
                    key={chip.id}
                    type="button"
                    onClick={() => submitQuestion(chip.query)}
                    className="min-h-[44px] px-3 py-1.5 rounded-xl bg-[var(--bg-surface)] hover:bg-[#D8F3DC]/40 dark:hover:bg-[#1B4332]/50 border border-[var(--border-default)] hover:border-[#2D6A4F] text-xs font-semibold text-[var(--text-primary)] text-left cursor-pointer transition-colors"
                  >
                    {chip.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Historique de la session */}
            {turns.map((turn) =>
              turn.role === 'user' ? (
                <div key={turn.id} className="flex justify-end">
                  <div className="max-w-[88%] px-3.5 py-2.5 rounded-2xl rounded-br-sm bg-[#1B4332] text-white text-xs sm:text-sm leading-relaxed break-words shadow-xs">
                    <p>{turn.text}</p>
                    <span className="block text-[10px] text-[#B7E4C7] text-right mt-1 font-mono">
                      {turn.createdAt}
                    </span>
                  </div>
                </div>
              ) : turn.reply ? (
                <div key={turn.id} className="flex justify-start">
                  <div className="max-w-[95%] p-3.5 rounded-2xl rounded-bl-sm bg-[var(--bg-surface)] border border-[var(--border-default)] text-xs sm:text-sm space-y-2.5 shadow-xs break-words">
                    <div className="font-bold text-[var(--text-primary)] leading-snug">
                      {turn.reply.headline}
                    </div>
                    <p className="text-[var(--text-muted)] leading-relaxed">
                      {turn.reply.body}
                    </p>
                    <ul className="space-y-1.5 list-disc pl-4 text-[var(--text-primary)]">
                      {turn.reply.bullets.map((bullet, idx) => (
                        <li key={idx} className="leading-snug">
                          {bullet}
                        </li>
                      ))}
                    </ul>

                    <div className="pt-1.5 flex flex-col gap-2">
                      {turn.reply.navAction && (
                        <button
                          type="button"
                          onClick={(e) => handleNavAction(turn.reply!.navAction!, e)}
                          className="min-h-[44px] w-full px-3 py-2 rounded-xl bg-[var(--brand-primary)] hover:bg-[var(--brand-primary-hover)] text-[var(--on-primary)] text-xs font-bold inline-flex items-center justify-between gap-2 cursor-pointer transition-colors"
                        >
                          <span className="text-left">{turn.reply.navAction.label}</span>
                          <ArrowUpRight className="w-4 h-4 shrink-0" />
                        </button>
                      )}

                      <a
                        href={turn.reply.whatsappUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="min-h-[44px] w-full px-3 py-2 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white border border-[#52B788]/40 text-xs font-bold inline-flex items-center justify-between gap-2 transition-colors"
                      >
                        <span className="inline-flex items-center gap-1.5 text-left">
                          <PhoneCall className="w-3.5 h-3.5 text-[#74C69D] shrink-0" />
                          <span>{turn.reply.whatsappLabel}</span>
                        </span>
                        <ArrowUpRight className="w-4 h-4 text-[#74C69D] shrink-0" />
                      </a>
                    </div>
                  </div>
                </div>
              ) : null
            )}
            <div ref={scrollEndRef} />
          </div>

          {/* Barre de saisie + lien direct WhatsApp */}
          <form
            onSubmit={handleFormSubmit}
            className="p-3 bg-[var(--bg-surface)] border-t border-[var(--border-default)] space-y-2"
          >
            <div className="flex items-center gap-2">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder={
                  lang === 'fr'
                    ? 'Posez votre question (tarifs, hôtel, salle...)'
                    : 'Ask about rates, hotels, 500-seat hall...'
                }
                aria-label={
                  lang === 'fr'
                    ? 'Votre question au Concierge Virtuel ECOPARK'
                    : 'Your question for the ECOPARK Virtual Concierge'
                }
                className="flex-1 min-w-0 min-h-[44px] px-3 py-2 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] text-xs sm:text-sm text-[var(--text-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--brand-primary)]"
              />
              <button
                type="submit"
                disabled={!inputValue.trim()}
                aria-label={lang === 'fr' ? 'Envoyer la question' : 'Send question'}
                className="min-h-[44px] min-w-[44px] px-3 rounded-xl bg-[var(--brand-primary)] hover:bg-[var(--brand-primary-hover)] disabled:opacity-45 text-[var(--on-primary)] inline-flex items-center justify-center cursor-pointer transition-colors shrink-0"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>

            <div className="flex items-center justify-between gap-2 text-[11px] text-[var(--text-muted)] px-0.5">
              <span>
                {lang === 'fr'
                  ? 'Session locale protégée (Loi 2024/017)'
                  : 'Protected local session (Law 2024/017)'}
              </span>
              <a
                href={defaultWhatsAppHref}
                target="_blank"
                rel="noreferrer"
                className="font-semibold text-[var(--brand-primary)] hover:underline inline-flex items-center gap-1"
              >
                <span>WhatsApp direct</span>
                <ArrowUpRight className="w-3 h-3" />
              </a>
            </div>
          </form>
        </div>
      )}

      {/* Bouton flottant d'ouverture du Concierge 24/7 */}
      <button
        ref={launcherRef}
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        aria-expanded={isOpen}
        aria-label={
          isOpen
            ? 'Concierge 24h/24 • FR/EN - Fermer la fenêtre'
            : 'Concierge 24h/24 • FR/EN - Poser une question ou réserver'
        }
        className="min-h-[50px] px-4 py-2.5 rounded-full bg-[#1B4332] hover:bg-[#2D6A4F] text-white border-2 border-[#74C69D]/70 shadow-xl inline-flex items-center gap-2.5 cursor-pointer transition-all focus-visible:ring-2 focus-visible:ring-[#74C69D]"
      >
        <span className="relative flex items-center justify-center">
          <MessageSquareText className="w-5 h-5 text-[#74C69D]" />
          <span
            aria-hidden="true"
            className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-emerald-400 border border-[#1B4332]"
          />
        </span>
        <span className="font-sans font-bold text-xs sm:text-sm tracking-tight whitespace-nowrap">
          Concierge 24h/24 • FR/EN
        </span>
      </button>
    </div>
  );
};
