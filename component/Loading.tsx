import React from 'react';
import { View, ActivityIndicator } from 'react-native';
import { useTailwind } from 'tailwind-rn/dist';

const Loading = () => {
    const tw = useTailwind();
    return (
        <View style={tw('flex-1 justify-center items-center')}>
            <ActivityIndicator size="large" color="blue" />
        </View>
    );
};

export default Loading;
