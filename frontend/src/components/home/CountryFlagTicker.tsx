"use client";

import * as Flags from "country-flag-icons/react/3x2";

// Purely decorative — the whole world, not tied to actual branch countries.
const COUNTRY_CODES = [
  "AF", "AL", "DZ", "AD", "AO", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB",
  "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "BI", "CV", "KH",
  "CM", "CA", "CF", "TD", "CL", "CN", "CO", "KM", "CR", "HR", "CU", "CY", "CZ", "CD", "DK",
  "DJ", "DM", "DO", "EC", "EG", "SV", "GQ", "ER", "EE", "SZ", "ET", "FJ", "FI", "FR", "GA",
  "GM", "GE", "DE", "GH", "GR", "GD", "GT", "GN", "GW", "GY", "HT", "HN", "HU", "IS", "IN",
  "ID", "IR", "IQ", "IE", "IL", "IT", "CI", "JM", "JP", "JO", "KZ", "KE", "KI", "KW", "KG",
  "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT",
  "MH", "MR", "MU", "MX", "FM", "MD", "MC", "MN", "ME", "MA", "MZ", "MM", "NA", "NR", "NP",
  "NL", "NZ", "NI", "NE", "NG", "KP", "MK", "NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY",
  "PE", "PH", "PL", "PT", "QA", "CG", "RO", "RU", "RW", "KN", "LC", "VC", "WS", "SM", "ST",
  "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "KR", "SS", "ES", "LK",
  "SD", "SR", "SE", "CH", "SY", "TW", "TJ", "TZ", "TH", "TL", "TG", "TO", "TT", "TN", "TR",
  "TM", "TV", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VU", "VA", "VE", "VN", "YE", "ZM",
  "ZW",
].filter((code) => code in Flags);

// Duplicated so the strip can loop seamlessly (animate 0 -> -50%)
const LOOPED_CODES = [...COUNTRY_CODES, ...COUNTRY_CODES];

export default function CountryFlagTicker() {
  return (
    <div
      className="relative overflow-hidden bg-paper py-6"
      style={{
        maskImage: "linear-gradient(to right, transparent, black 8%, black 92%, transparent)",
        WebkitMaskImage: "linear-gradient(to right, transparent, black 8%, black 92%, transparent)",
      }}
    >
      <div className="flex w-max animate-marquee gap-6 motion-reduce:animate-none hover:[animation-play-state:paused]">
        {LOOPED_CODES.map((code, i) => {
          const Flag = (Flags as Record<string, React.ComponentType<{ title?: string }>>)[code];
          return (
            <span
              key={`${code}-${i}`}
              className="block w-10 shrink-0 overflow-hidden rounded-[3px] border border-navy/10 shadow-sm"
            >
              <Flag title={code} />
            </span>
          );
        })}
      </div>
    </div>
  );
}
