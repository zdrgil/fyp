import AsyncStorage from '@react-native-async-storage/async-storage';
import { CompositeNavigationProp, useIsFocused, useNavigation } from '@react-navigation/native';
import React, { useState, useCallback, useEffect, useLayoutEffect } from 'react';
import { View, Text, StyleSheet, Image, KeyboardAvoidingView, ScrollView, Button } from 'react-native';
import { GiftedChat } from 'react-native-gifted-chat';
import Separator from '../component/Separator';
import { TabStackParamList } from '../Navtor/TabNavtor';
import { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootstackParamList } from '../Navtor/RootNavtor';
import Loading from '../component/Loading';

const RASA_URL = 'http://192.168.110.91:5005/webhooks/rest/webhook';
export type CustomerScreenNavigationProp = CompositeNavigationProp<
    BottomTabNavigationProp<TabStackParamList, 'Customer'>,
    NativeStackNavigationProp<RootstackParamList>
>
const ChatbotScreen = () => {
    const navigation = useNavigation<CustomerScreenNavigationProp>();
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [loggedIn, setLoggedIn] = useState(false);
    const [loading, setLoading] = useState<boolean>(false);
    const [userData, setUserData] = useState<any>(null);
    const isFocused = useIsFocused();

    useLayoutEffect(() => {
        navigation.setOptions({
            headerStyle: {
                backgroundColor: 'rgba(89, 193, 204,1)'
            }


        })
    }, []);

    const sendMessage = useCallback(async () => {
        try {
            const response = await fetch(RASA_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: inputText,
                    sender: userData.id
                }),
            });

            const data = await response.json();

            // 將接收到的消息加入到聊天記錄中
            setMessages(previousMessages =>
                GiftedChat.append(
                    previousMessages,
                    data.map(({ text, image, sender }) => {
                        if (image) {
                            // 如果訊息中包含圖片，創建圖片消息對象
                            return {
                                _id: Math.random().toString(36).substring(7),
                                image,
                                createdAt: new Date(),
                                user: { _id: sender, name: sender },
                            };
                        } else {
                            // 否則顯示純文字訊息
                            return {
                                _id: Math.random().toString(36).substring(7),
                                text,
                                createdAt: new Date(),
                                user: { _id: sender, name: sender },
                            };
                        }
                    }),
                ),
            );
        } catch (error) {
            console.error(error);
        }
    }, [inputText, userData]);


    const fetchStoredData = async () => {
        try {
            const storedData = await AsyncStorage.getItem('usersData');
            if (storedData) {
                const parsedData = JSON.parse(storedData);
                setUserData(parsedData);

                setLoading(false);
            }
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        setLoading(true);
        AsyncStorage.getItem('loggedIn').then(async value => {
            if (value === 'true') {
                setLoggedIn(true);
                fetchStoredData();

            } else if (value === 'false') {
                setLoggedIn(false);
            }
        });
    }, [isFocused]);

    if (loading) {
        setTimeout(() => {
            setLoading(false);

        }, 700); // 0.5秒的延迟时间
        return <Loading />;
    }

    if (!userData) {

    }




    return (
        <>
            {loggedIn ? (<View style={{ flex: 1, padding: 2 }}>
                <GiftedChat

                    messages={messages}
                    onSend={messages => {
                        // 將用戶輸入的消息加入到聊天記錄中
                        setMessages(previousMessages =>
                            GiftedChat.append(previousMessages, messages),
                        );

                        // 發送消息給 Rasa 服務器
                        setInputText(messages[0].text);
                        sendMessage();
                        setInputText('');
                    }}
                    user={{
                        _id: 'me'
                    }}
                    placeholder="Message.."
                    text={inputText}
                    onInputTextChanged={setInputText}
                    renderMessageImage={({ currentMessage }) => (
                        <Image
                            source={{ uri: currentMessage.image }}
                            style={{ width: 300, height: 200 }}
                        />
                    )}

                    renderAvatar={({ currentMessage }) => {
                        if (!currentMessage.user) {
                            return null;
                        }
                        if (currentMessage.user._id === 'bot') {
                            return (
                                <Image
                                    source={require('../assets/chatboticon.png')}
                                    style={{ width: 40, height: 40, borderRadius: 20 }}
                                />
                            );
                        } else {
                            return (
                                <Image
                                    source={require('../assets/chatboticon.png')}
                                    style={{ width: 40, height: 40, borderRadius: 20 }}
                                />
                            );
                        }
                    }}
                />

            </View>) : (<KeyboardAvoidingView behavior="position" style={styles.contentContainerStyle}>
                <Image
                    source={require('../assets/chatboticon.png')}
                    style={{ width: 430, height: 420 }}
                />
                <ScrollView contentContainerStyle={styles.contentContainerStyle}>
                    <Text>Login first:</Text>
                    <Button title="Login" onPress={() => navigation.navigate('Login')} />
                    <Separator />
                    <Button title="Register" onPress={() => navigation.navigate('Register')} />
                    <Separator />
                </ScrollView>
                <View style={{ height: 20 }} />
            </KeyboardAvoidingView>)}
        </>

    );
};

export default ChatbotScreen;

const styles = StyleSheet.create({
    container: {},
    imputContainer: {
        width: 320,
    },
    contentContainerStyle: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 0,
        backgroundColor: "#bee9f7",
    },

    separator: {
        marginVertical: 8,
        borderBottomColor: '#737373',
        borderBottomWidth: StyleSheet.hairlineWidth,
        width: 300,
    },
    button: {
        backgroundColor: "white"

    },

});