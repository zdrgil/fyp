import React, { useLayoutEffect, useState } from 'react'
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs"
import Customerscreen from '../screen/CustomerScreen'
import OrderScreen from '../screen/OrderScreen'
import { useNavigation } from '@react-navigation/native'
import { Icon } from '@rneui/base'
import LoginScreen from '../screen/LoginScreen'
import { createStackNavigator } from '@react-navigation/stack'
import ChatbotScreen from '../screen/ChatbotScreen'


export type TabStackParamList = {
    Customer: undefined;
    Order: undefined;
    Login: undefined;
    Chatbot: undefined;

}

const Tab = createBottomTabNavigator<TabStackParamList>();
const Stack = createStackNavigator();



const TabNavtor = () => {
    const navigation = useNavigation();

    useLayoutEffect(() => {
        navigation.setOptions({
            headerShown: false,
        })
    }, []);

    return (
        <Tab.Navigator
            screenOptions={({ route }) => ({
                tabBarActiveTintColor: "#59C1CC",
                tabBarInactiveTintColor: "gray",
                tabBarIcon: ({ focused, color, size }) => {
                    if (route.name === 'Customer') {
                        return (
                            <Icon
                                name="users"
                                type="entypo"
                                color={focused ? "#59C1CC" : "gray"}
                            />
                        );
                    } else if (route.name === 'Order') {
                        return (
                            <Icon
                                name="box"
                                type="entypo"
                                color={focused ? "#59C1CC" : "gray"}
                            />
                        )

                    } else if (route.name === 'Login') {
                        return (
                            <Icon
                                name="login"
                                type="entypo"
                                color={focused ? "#59C1CC" : "gray"}
                            />
                        )

                    } else if (route.name === 'Chatbot') {
                        return (
                            <Icon
                                name="login"
                                type="entypo"
                                color={focused ? "#59C1CC" : "gray"}
                            />
                        )

                    }

                }



            })}>
            <Tab.Screen name="Customer" component={Customerscreen} />
            <Tab.Screen name="Order" component={OrderScreen} />
            <Tab.Screen name="Login" component={LoginScreen}
            />
            <Tab.Screen name="Chatbot" component={ChatbotScreen} />

        </Tab.Navigator>

    );
};

export default TabNavtor;