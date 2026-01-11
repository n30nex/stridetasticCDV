'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import { User } from '@/types';
import { apiClient } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isPrivileged: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user;
  const isPrivileged = Boolean(user && (user.is_staff || user.is_superuser));

  useEffect(() => {
    const loadUser = async () => {
      const accessToken = Cookies.get('access_token');
      if (!accessToken) {
        setUser(null);
        setIsLoading(false);
        return;
      }

      try {
        const response = await apiClient.getCurrentUser();
        setUser(response.data);
      } catch (error) {
        console.error('Failed to load user profile:', error);
        apiClient.logout();
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    loadUser();
  }, []);

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      const response = await apiClient.login({ username, password });
      const { access, refresh } = response.data;

      // Store tokens in cookies
      Cookies.set('access_token', access, { expires: 1 }); // 1 day
      Cookies.set('refresh_token', refresh, { expires: 7 }); // 7 days

      try {
        const me = await apiClient.getCurrentUser();
        setUser(me.data);
      } catch (error) {
        console.error('Failed to fetch user profile after login:', error);
        apiClient.logout();
        setUser(null);
        return false;
      }

      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  };

  const logout = () => {
    apiClient.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated,
      isPrivileged,
      isLoading,
      login,
      logout,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
