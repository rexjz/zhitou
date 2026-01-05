import React, { useEffect, useState, useRef, useCallback } from 'react';
import { List, Skeleton, Typography, Space, Tag } from 'antd';
import { useGetCurrentUserSessions as useGetCurrentUserAgentChatSessions } from "@/sdk/agent/agent";
import type { SessionData } from "@/sdk/models/sessionData";

const { Text } = Typography;

const PAGE_SIZE = 10;

interface SessionItemProps extends SessionData {
  loading?: boolean;
}

interface SessionListViewProps {
  onSessionClick?: (session: SessionData, index: number) => void;
}

function SessionListView({ onSessionClick }: SessionListViewProps) {
  const [page, setPage] = useState(1);
  const [allSessions, setAllSessions] = useState<SessionData[]>([]);
  const [hasMore, setHasMore] = useState(true);
  const loadMoreRef = useRef<HTMLDivElement>(null);
  const observerRef = useRef<IntersectionObserver | null>(null);

  // Fetch data with current page
  const { data, isLoading, error } = useGetCurrentUserAgentChatSessions({
    page_size: PAGE_SIZE,
    page_number: page,
    sort_order: 'desc'
  });

  // Update sessions list when data changes
  useEffect(() => {
    if (data?.data?.data?.sessions) {
      const newSessions = data.data.data.sessions;
      const total = data.data.data.total;

      setAllSessions((prev) => {
        // Avoid duplicates by filtering out existing session IDs
        const existingIds = new Set(prev.map(s => s.session_id));
        const uniqueNew = newSessions.filter(s => !existingIds.has(s.session_id));
        return [...prev, ...uniqueNew];
      });

      // Check if we have more data to load
      setHasMore(allSessions.length + newSessions.length < total);
    }
  }, [data]);

  // Set up IntersectionObserver for infinite scroll
  const handleObserver = useCallback((entries: IntersectionObserverEntry[]) => {
    const target = entries[0];
    if (target.isIntersecting && hasMore && !isLoading) {
      setPage((prev) => prev + 1);
    }
  }, [hasMore, isLoading]);

  useEffect(() => {
    const option = {
      root: null,
      rootMargin: '20px',
      threshold: 0
    };

    observerRef.current = new IntersectionObserver(handleObserver, option);

    if (loadMoreRef.current) {
      observerRef.current.observe(loadMoreRef.current);
    }

    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect();
      }
    };
  }, [handleObserver]);

  // Format timestamp
  const formatDate = (timestamp: number) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleString();
  };

  // Prepare list data with loading placeholders
  const listData: SessionItemProps[] = isLoading && page === 1
    ? Array.from({ length: PAGE_SIZE }).map((_, index) => ({
        loading: true,
      } as SessionItemProps))
    : allSessions;

  if (error) {
    return <div>Error loading sessions: {error.message}</div>;
  }

  return (
    <div style={{ height: '100%', overflow: 'auto' }}>
      <List
        itemLayout="horizontal"
        dataSource={listData}
        loading={isLoading && page === 1}
        renderItem={(item, index) => (
          <List.Item
            onClick={() => {
              if (!item.loading && onSessionClick) {
                onSessionClick(item as SessionData, index);
              }
            }}
            style={{
              cursor: item.loading ? 'default' : 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseEnter={(e) => {
              if (!item.loading) {
                e.currentTarget.style.backgroundColor = '#f5f5f5';
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'transparent';
            }}
          >
            <Skeleton loading={item.loading} active avatar>
              <List.Item.Meta
                title={
                  <Space>
                    <Text strong>{item.session_type}</Text>
                    <Tag color="blue">{item.agent_id}</Tag>
                  </Space>
                }
                description={
                  <Space direction="vertical" size="small">
                    <Text type="secondary">Session ID: {item.session_id}</Text>
                    {item.summary && <Text>{item.summary}</Text>}
                    <Text type="secondary" style={{ fontSize: '12px' }}>
                      Created: {formatDate(item.created_at)} | Updated: {formatDate(item.updated_at)}
                    </Text>
                  </Space>
                }
              />
            </Skeleton>
          </List.Item>
        )}
      />

      {/* Loading indicator for infinite scroll */}
      {hasMore && (
        <div
          ref={loadMoreRef}
          style={{
            textAlign: 'center',
            padding: '20px',
            color: '#999'
          }}
        >
          {isLoading && page > 1 ? 'Loading more sessions...' : ''}
        </div>
      )}

      {!hasMore && allSessions.length > 0 && (
        <div style={{ textAlign: 'center', padding: '20px', color: '#999' }}>
          No more sessions to load
        </div>
      )}
    </div>
  );
}

export default SessionListView;