import React, { useState } from 'react';
import { ScrollView, RefreshControl } from 'react-native';

const Refresh = (props) => {
    const [refreshing, setRefreshing] = useState(false);

    const onRefresh = React.useCallback(() => {
        setRefreshing(true);
        props.onRefresh().finally(() => {
            setTimeout(() => {
                setRefreshing(false); // 在 0.5 秒后关闭下拉刷新效果
            }, 1000);
        });
    }, [props]);

    return (
        <ScrollView refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}>
            {props.children}
        </ScrollView>
    );
};

export default Refresh;