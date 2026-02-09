import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { Menu, X, Home, MessageCircle, User, LogOut } from 'lucide-react';

const Navbar = ({ darkMode }) => {
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check if user is logged in by checking for tokens
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);

    // Close menu when route changes
    const handleRouteChange = () => {
      setIsMenuOpen(false);
    };

    router.events.on('routeChangeComplete', handleRouteChange);
    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    router.push('/login');
  };

  const navLinks = isLoggedIn
    ? [
        { href: '/', label: 'Home', icon: Home },
        { href: '/chat', label: 'Chat', icon: MessageCircle },
      ]
    : [];

  const authLinks = isLoggedIn
    ? [
        { href: '#', label: 'Logout', icon: LogOut, onClick: handleLogout },
      ]
    : [
        { href: '/login', label: 'Login', icon: User },
        { href: '/register', label: 'Register', icon: User },
      ];

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 backdrop-blur-lg border-b ${
      darkMode
        ? 'bg-white/10 border-white/20'
        : 'bg-white/80 border-slate-200'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
              darkMode ? 'bg-gradient-to-r from-purple-500 to-blue-500' : 'bg-gradient-to-r from-purple-500 to-blue-500'
            }`}>
              <span className="text-white font-bold text-sm">T</span>
            </div>
            <span className={`font-bold text-lg ${
              darkMode ? 'text-white' : 'text-gray-900'
            }`}>
              TaskFlow
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => {
              const IconComponent = link.icon;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors duration-200 ${
                    router.pathname === link.href
                      ? darkMode
                        ? 'bg-white/20 text-white'
                        : 'bg-gray-100 text-gray-900'
                      : darkMode
                      ? 'text-slate-300 hover:text-white hover:bg-white/10'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <IconComponent size={18} />
                  <span>{link.label}</span>
                </Link>
              );
            })}

            {authLinks.map((link) => {
              const IconComponent = link.icon;
              return (
                <div key={link.href}>
                  {link.onClick ? (
                    <button
                      onClick={link.onClick}
                      className={`flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors duration-200 ${
                        darkMode
                          ? 'text-slate-300 hover:text-white hover:bg-white/10'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                      }`}
                    >
                      <IconComponent size={18} />
                      <span>{link.label}</span>
                    </button>
                  ) : (
                    <Link
                      href={link.href}
                      className={`flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors duration-200 ${
                        router.pathname === link.href
                          ? darkMode
                            ? 'bg-white/20 text-white'
                            : 'bg-gray-100 text-gray-900'
                          : darkMode
                          ? 'text-slate-300 hover:text-white hover:bg-white/10'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                      }`}
                    >
                      <IconComponent size={18} />
                      <span>{link.label}</span>
                    </Link>
                  )}
                </div>
              );
            })}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className={`p-2 rounded-lg ${
                darkMode
                  ? 'text-slate-300 hover:text-white hover:bg-white/10'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className={`md:hidden border-t ${
          darkMode
            ? 'bg-white/10 border-white/20'
            : 'bg-white/80 border-slate-200'
        }`}>
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navLinks.map((link) => {
              const IconComponent = link.icon;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center space-x-2 w-full px-3 py-2 rounded-lg transition-colors duration-200 ${
                    router.pathname === link.href
                      ? darkMode
                        ? 'bg-white/20 text-white'
                        : 'bg-gray-100 text-gray-900'
                      : darkMode
                      ? 'text-slate-300 hover:text-white hover:bg-white/10'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <IconComponent size={18} />
                  <span>{link.label}</span>
                </Link>
              );
            })}
            {authLinks.map((link) => {
              const IconComponent = link.icon;
              return (
                <div key={link.href}>
                  {link.onClick ? (
                    <button
                      onClick={link.onClick}
                      className={`flex items-center space-x-2 w-full px-3 py-2 rounded-lg transition-colors duration-200 ${
                        darkMode
                          ? 'text-slate-300 hover:text-white hover:bg-white/10'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                      }`}
                    >
                      <IconComponent size={18} />
                      <span>{link.label}</span>
                    </button>
                  ) : (
                    <Link
                      href={link.href}
                      className={`flex items-center space-x-2 w-full px-3 py-2 rounded-lg transition-colors duration-200 ${
                        router.pathname === link.href
                          ? darkMode
                            ? 'bg-white/20 text-white'
                            : 'bg-gray-100 text-gray-900'
                          : darkMode
                          ? 'text-slate-300 hover:text-white hover:bg-white/10'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                      }`}
                    >
                      <IconComponent size={18} />
                      <span>{link.label}</span>
                    </Link>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;