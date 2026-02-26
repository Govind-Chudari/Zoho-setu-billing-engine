import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {
  LayoutDashboard, FolderOpen, BarChart2,
  Receipt, LogOut, Zap, ChevronRight, Menu, X
} from "lucide-react";
import { useState } from "react";

const NAV = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/files",     icon: FolderOpen,      label: "My Files"  },
  { to: "/usage",     icon: BarChart2,        label: "Usage"     },
  { to: "/billing",   icon: Receipt,          label: "Billing"   },
];

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const initials = user?.username?.slice(0, 2).toUpperCase() || "??";

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <>
      {/* DESKTOP SIDEBAR  (lg and above)*/}
      <aside className="hidden lg:flex w-56 bg-brand-900 flex-col
                        min-h-screen sticky top-0 shrink-0">

        {/* Logo */}
        <div className="px-5 py-6 border-b border-white/10">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center">
              <Zap size={17} className="text-white" />
            </div>
            <div>
              <div className="text-white font-extrabold text-lg tracking-tight leading-none">
                BillFlow
              </div>
              <div className="text-blue-400 text-[10px] font-medium mt-0.5">
                Billing Engine
              </div>
            </div>
          </div>
        </div>

        {/* Section label */}
        <div className="px-5 pt-5 pb-2">
          <span className="text-[10px] font-bold text-white/30 uppercase tracking-widest">
            Navigation
          </span>
        </div>

        {/* links */}
        <nav className="flex-1 px-3 pb-4 space-y-0.5">
          {NAV.map(({ to, icon: Icon, label }) => (
            <NavLink key={to} to={to}>
              {({ isActive }) => (
                <div className={`flex items-center gap-3 px-3 py-2.5 rounded-xl
                                 text-sm font-medium transition-all duration-150 group
                                 ${isActive
                                   ? "bg-brand-600 text-white shadow-lg shadow-brand-600/30"
                                   : "text-white/60 hover:text-white hover:bg-white/8"
                                 }`}>
                  <Icon size={17} className={
                    isActive
                      ? "text-white"
                      : "text-white/50 group-hover:text-white/80"
                  } />
                  <span className="flex-1">{label}</span>
                  {isActive && <ChevronRight size={14} className="text-white/60" />}
                </div>
              )}
            </NavLink>
          ))}
        </nav>

        {/* Plan badge */}
        <div className="mx-3 mb-4 bg-gradient-to-r from-brand-700 to-brand-600
                         rounded-xl px-4 py-3 border border-brand-500/40">
          <div className="text-white text-xs font-bold mb-0.5">Free Plan</div>
          <div className="text-blue-300 text-[11px]">1 GB storage included</div>
          <div className="mt-2 h-1.5 bg-white/20 rounded-full overflow-hidden">
            <div className="h-full w-1/5 bg-white rounded-full" />
          </div>
          <div className="text-blue-300 text-[10px] mt-1">200 MB / 1 GB used</div>
        </div>

        {/* User + logout */}
        <div className="px-3 pb-5 pt-3 border-t border-white/10 space-y-2">
          <div className="flex items-center gap-3 px-2 py-2">
            <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center
                            justify-center text-white text-xs font-bold shrink-0">
              {initials}
            </div>
            <div className="min-w-0">
              <div className="text-white text-sm font-semibold truncate">
                {user?.username}
              </div>
              <div className="text-blue-400 text-[11px]">Free account</div>
            </div>
          </div>
          <button onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 py-2.5 px-3
                       rounded-xl bg-red-500/10 hover:bg-red-500/20
                       border border-red-500/20
                       text-red-400 hover:text-red-300 text-sm font-semibold
                       transition-all duration-150">
            <LogOut size={15} />
            Sign Out
          </button>
        </div>
      </aside>

      {/* TABLET TOP BAR  (md only, 768–1023px) */}
      <div className="hidden md:flex lg:hidden fixed top-0 left-0 right-0 z-40
                      bg-brand-900 border-b border-white/10 h-14
                      items-center justify-between px-4">

        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 bg-brand-600 rounded-lg flex items-center justify-center">
            <Zap size={15} className="text-white" />
          </div>
          <span className="text-white font-extrabold text-base tracking-tight">
            BillFlow
          </span>
        </div>

        {/* Tablet nav links */}
        <nav className="flex items-center gap-1">
          {NAV.map(({ to, icon: Icon, label }) => (
            <NavLink key={to} to={to}>
              {({ isActive }) => (
                <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg
                                 text-xs font-semibold transition-all
                                 ${isActive
                                   ? "bg-brand-600 text-white"
                                   : "text-white/60 hover:text-white hover:bg-white/10"
                                 }`}>
                  <Icon size={14} />
                  <span className="hidden sm:inline">{label}</span>
                </div>
              )}
            </NavLink>
          ))}
        </nav>

        {/* Right: avatar + logout */}
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-brand-600 flex items-center
                          justify-center text-white text-xs font-bold">
            {initials}
          </div>
          <button onClick={handleLogout}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg
                       bg-red-500/10 border border-red-500/20
                       text-red-400 hover:bg-red-500/20 text-xs font-semibold
                       transition-all">
            <LogOut size={13} />
            <span className="hidden sm:inline">Sign Out</span>
          </button>
        </div>
      </div>

      {/* MOBILE BOTTOM TAB BAR  (< 768px) */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-40
                      bg-brand-900 border-t border-white/10
                      flex items-center justify-around px-2 py-2
                      safe-area-inset-bottom">
        {NAV.map(({ to, icon: Icon, label }) => (
          <NavLink key={to} to={to}>
            {({ isActive }) => (
              <div className={`flex flex-col items-center gap-0.5 px-4 py-1.5
                               rounded-xl transition-all duration-150 min-w-0
                               ${isActive
                                 ? "text-brand-400"
                                 : "text-white/40"
                               }`}>
                {isActive && (
                  <div className="absolute -top-0.5 w-8 h-0.5 bg-brand-400 rounded-full" />
                )}
                <Icon size={20} />
                <span className="text-[10px] font-semibold truncate">{label}</span>
              </div>
            )}
          </NavLink>
        ))}

        {/* Logout in bottom bar */}
        <button onClick={handleLogout}
          className="flex flex-col items-center gap-0.5 px-4 py-1.5
                     text-red-400/70 transition-all">
          <LogOut size={20} />
          <span className="text-[10px] font-semibold">Logout</span>
        </button>
      </div>

      {/* Mobile top header — just logo */}
      <div className="md:hidden fixed top-0 left-0 right-0 z-40
                      bg-brand-900 border-b border-white/10 h-12
                      flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-brand-600 rounded-md flex items-center justify-center">
            <Zap size={13} className="text-white" />
          </div>
          <span className="text-white font-extrabold text-base tracking-tight">
            BillFlow
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-brand-600 flex items-center
                          justify-center text-white text-xs font-bold">
            {initials}
          </div>
        </div>
      </div>
    </>
  );
}