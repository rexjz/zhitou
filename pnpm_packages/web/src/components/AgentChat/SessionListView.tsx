import { useEffect, useState, useRef, useCallback } from 'react';
import { List, Skeleton, Typography, Space, Tag, Button } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import { useGetCurrentUserSessions as useGetCurrentUserAgentChatSessions } from "@/sdk/agent/agent";
import type { SessionData } from "@/sdk/models/sessionData";

const { Text } = Typography;

const PAGE_SIZE = 10;

interface SessionItemProps extends SessionData {
  loading?: boolean;
}

interface SessionListViewProps {
  onSessionClick?: (session: SessionData, index: number) => void;
  activatedSessionId?: string | null;
}

function SessionListView({ onSessionClick, activatedSessionId }: SessionListViewProps) {
  const [page, setPage] = useState(1);
  const [allSessions, setAllSessions] = useState<SessionData[]>([]);
  const [hasMore, setHasMore] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const loadMoreRef = useRef<HTMLDivElement>(null);
  const observerRef = useRef<IntersectionObserver | null>(null);

  // Fetch data with current page
  const { data, isLoading, error, mutate } = useGetCurrentUserAgentChatSessions({
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

  // Refresh sessions
  const handleRefresh = async () => {
    setIsRefreshing(true);
    setAllSessions([]);
    setPage(1);
    setHasMore(true);
    try {
      await mutate();
    } finally {
      setIsRefreshing(false);
    }
  };

  // Prepare list data with loading placeholders
  const listData: SessionItemProps[] = isLoading && page === 1
    ? Array.from({ length: PAGE_SIZE }).map(() => ({
        loading: true,
      } as SessionItemProps))
    : allSessions;

  if (error) {
    return <div>Error loading sessions: {error.message}</div>;
  }

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Toolbar with refresh button */}
      <div style={{
        padding: '12px 16px',
        borderBottom: '1px solid #f0f0f0',
        display: 'flex',
        justifyContent: 'flex-end'
      }}>
        <Button
          type="text"
          icon={<ReloadOutlined />}
          onClick={handleRefresh}
          loading={isRefreshing}
          size="small"
        >
          刷新
        </Button>
      </div>

      {/* Sessions list */}
      <div style={{ flex: 1, overflow: 'auto' }}>
        <List
        itemLayout="horizontal"
        dataSource={listData}
        loading={isLoading && page === 1}
        renderItem={(item, index) => {
          const isActivated = !item.loading && item.session_id === activatedSessionId;
          return (
            <List.Item
              onClick={() => {
                if (!item.loading && onSessionClick) {
                  onSessionClick(item as SessionData, index);
                }
              }}
              style={{
                cursor: item.loading ? 'default' : 'pointer',
                transition: 'background-color 0.2s, border-color 0.2s',
                backgroundColor: isActivated ? '#e6f4ff' : 'transparent',
                borderLeft: isActivated ? '4px solid #1890ff' : '4px solid transparent',
                paddingLeft: isActivated ? '12px' : '16px'
              }}
              onMouseEnter={(e) => {
                if (!item.loading && !isActivated) {
                  e.currentTarget.style.backgroundColor = '#f5f5f5';
                }
              }}
              onMouseLeave={(e) => {
                if (!isActivated) {
                  e.currentTarget.style.backgroundColor = 'transparent';
                }
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
                    {item.summary && <Text>{item.summary}</Text>}
                    <Text type="secondary">
                      创建于: {formatDate(item.created_at)} 
                    </Text>
                  </Space>
                }
              />
            </Skeleton>
          </List.Item>
          );
        }}
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
    </div>
  );
}

export default SessionListView;