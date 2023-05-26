import React, { useState, useEffect, useLayoutEffect } from 'react';
import { View, Text, TextInput, Button, RefreshControl, ScrollView, ActivityIndicator, StyleSheet, KeyboardAvoidingView } from 'react-native';
import axios from 'axios';
import base64 from 'react-native-base64';
import { useTailwind } from 'tailwind-rn/dist';
import { Image, Input } from '@rneui/themed';
import { CompositeNavigationProp, useIsFocused, useNavigation } from '@react-navigation/native';
import { TabStackParamList } from '../Navtor/TabNavtor';
import { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootstackParamList } from '../Navtor/RootNavtor';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Loading from '../component/Loading';


export type CustomerScreenNavigationProp = CompositeNavigationProp<
    BottomTabNavigationProp<TabStackParamList, 'Customer'>,
    NativeStackNavigationProp<RootstackParamList>
>

interface IUser {
    url: string;
    id: number;
    username: string;
    email: string;
    is_staff: boolean;
    customer: {
        id: string;
        fullname: string;
        age: number;
        sex: string;
        phonenumber: string;
    };
}
interface IAppointment {
    id: number;
    date: string;
    time: string;
    fullname: string;
    age: number;
    sex: string;
    state: string;
    doctor: number;
    customer: number;
    clinic: number;
}


const Separator = () => <View style={styles.separator} />;

const LoginScreen = () => {
    const tw = useTailwind();
    const isFocused = useIsFocused();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loggedIn, setLoggedIn] = useState(false);
    const [refreshing, setRefreshing] = useState<boolean>(false);
    const [users, setUsers] = useState<IUser[]>([]);
    const [appointments, setAppointments] = useState<IAppointment[]>([]);
    const navigation = useNavigation<CustomerScreenNavigationProp>();
    const [loading, setLoading] = useState<boolean>(false);



    const fetchUsers = async () => {
        try {
            const response = await axios.get('http://192.168.110.91:8000/api/users/get_current_user/', {

            });
            setUsers([response.data])
            const usersData = response.data
            AsyncStorage.setItem('usersData', JSON.stringify(usersData));
            //console.log('Current', usersData)


        } catch (error) {
            console.error(error);
        }
        setRefreshing(false);
    };



    const fetchAppointment = async () => {
        try {
            const storedUserData = await AsyncStorage.getItem('usersData');
            if (storedUserData) {
                const userData = JSON.parse(storedUserData);
                const appointmentUrl = `http://192.168.110.91:8000/api/appointments/customer/${userData.customer.id}`;
                const response = await axios.get<IAppointment[]>(appointmentUrl);
                setAppointments(response.data);
                const appointments = response.data
                AsyncStorage.setItem('appointments', JSON.stringify(appointments));

            } else {
                console.log('No user data found in AsyncStorage.');
            }
        } catch (error) {
            console.error(error);
        }
        setRefreshing(false);
    };



    const handleLogin = async () => {
        setLoading(true);

        try {
            // 获取新的 CSRF Token
            const response1 = await axios.get('http://192.168.110.91:8000/api/get_csrf_token/');
            const newCSRFToken = response1.data.csrf_token;
            //console.log('New CSRF Token:', newCSRFToken);

            // 发送登录请求
            const authHeader = 'Basic ' + base64.encode(username + ':' + password);

            const response2 = await axios.post(
                'http://192.168.110.91:8000/api/login/',
                {
                    username: username,
                    password: password,
                },
                {
                    headers: {
                        Authorization: authHeader,
                        'X-CSRFToken': newCSRFToken, // 使用新的 CSRF Token
                    },
                }
            );

            fetchUsers();
            fetchAppointment();
            AsyncStorage.setItem('loggedIn', 'true');
            AsyncStorage.setItem('username', username);
            AsyncStorage.setItem('password', password);
            printAsyncStorageData();
            setLoggedIn(true);
        } catch (error) {
            console.log(error);
            alert('Username or password wrong');
        }
    };

    const handleLogout = async () => {
        setLoading(true);

        try {
            //获取新的 CSRF Token
            const response1 = await axios.get('http://192.168.110.91:8000/api/get_csrf_token/');
            let newCSRFToken = response1.data.csrf_token;
            //console.log('New CSRF Token:', newCSRFToken);
            // 发送注销请求
            const authHeader = 'Basic ' + base64.encode(username + ':' + password);
            const response2 = await axios.post(
                'http://192.168.110.91:8000/api/logout/',
                {
                    username: username,
                    password: password,
                },
                {
                    headers: {
                        Authorization: authHeader,
                        'X-CSRFToken': newCSRFToken, // 使用新的 CSRF Token
                    },
                }
            );

            AsyncStorage.setItem('loggedIn', 'false')
            AsyncStorage.setItem('username', '')
            AsyncStorage.setItem('password', '')

            printAsyncStorageData();

            setUsers([]);
            setAppointments([]);
            AsyncStorage.setItem('usersData', '');
            AsyncStorage.setItem('appointments', '');


            setLoggedIn(false);
            // console.log('Logout response:', response2.data);
        } catch (error) {
            if (error.response) {
                //console.log('Response data:', error.response.data);
                //console.log('Response status:', error.response.status);
                //console.log('Response headers:', error.response.headers);
            } else if (error.request) {
                //console.log('Request:', error.request);
            } else {
                //console.log('Error message:', error.message);
            }
        }
    };


    const onRefresh = React.useCallback(() => {
        setRefreshing(true);
        fetchUsers();
        fetchAppointment();
        printAsyncStorageData();
        console.log('Login Status:-------------------------', loggedIn)

    }, []);

    useEffect(() => {
        navigation.setOptions({
            headerShown: false,
        });

        AsyncStorage.getItem('loggedIn').then(value => {
            if (value === 'true') {
                setLoggedIn(true);
                fetchUsers(); // 获取用户数据

                // 执行其他操作，例如打印用户数据
                printAsyncStorageData();
                console.log('Login Status:', loggedIn);
            } else {
                setLoggedIn(false);
            }
        });





    }, [isFocused]);

    const printAsyncStorageData = async () => {
        try {
            const keys = await AsyncStorage.getAllKeys();
            const items = await AsyncStorage.multiGet(keys);

            console.log('AsyncStorage Data[]:')
            items.forEach(([key, value]) => {
                console.log(key, value);
            });
        } catch (error) {
            console.error(error);
        }
    };

    if (loading) {
        setTimeout(() => {
            setLoading(false);
        }, 700); // 0.5秒的延迟时间
        return <Loading />;
    }





    return (
        <>
            {loggedIn ? (
                <KeyboardAvoidingView behavior="padding" style={styles.contentContainerStyle}>
                    <ScrollView contentContainerStyle={styles.contentContainerStyle}

                        refreshControl={
                            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
                        }
                    >
                        <View style={styles.header}>
                            <Image style={styles.avatar} source={{ uri: 'https://www.bootdey.com/img/Content/avatar/avatar6.png' }} />
                            <View style={styles.info}>
                                <Text style={styles.name}>{users.length > 0 ? users[0].username : ''}</Text>
                                <Text style={styles.username}>Your ID @{users.length > 0 ? users[0].id : ''}</Text>
                            </View>
                        </View>

                        <View style={styles.card}>
                            <Text style={styles.cardTittle}>Your infomation</Text>
                            <Text>Age: {users.length > 0 ? users[0].customer.age : ''}</Text>
                            <Text>phonenumber: {users.length > 0 ? users[0].customer.phonenumber : ''}</Text>
                            <Text>sex: {users.length > 0 ? users[0].customer.sex : ''}</Text>
                            <Text>email: {users.length > 0 ? users[0].email : ''}</Text>
                            <Text>fullname: {users.length > 0 ? users[0].customer.fullname : ''}</Text>
                        </View>

                        <View style={styles.card2}>
                            <ScrollView>
                                {appointments.map(appointment => (
                                    <View key={appointment.id} style={styles.appointmentItem}>
                                        <Text>Date: {appointment.date}</Text>
                                        <Text>Time: {appointment.time}</Text>
                                        <Text>state: {appointment.state}</Text>
                                        <Text>clinic: {appointment.clinic}</Text>


                                        <Separator />

                                        {/* 渲染其他属性 */}
                                    </View>
                                ))}
                            </ScrollView>

                        </View>


                        <Button title="Logout" onPress={handleLogout} />

                        <Separator />
                    </ScrollView>
                </KeyboardAvoidingView>
            ) : (

                <KeyboardAvoidingView behavior="position" style={styles.contentContainerStyle}>
                    <Image
                        source={require('../assets/Login.png')}
                        style={{ width: 430, height: 280 }}

                    />

                    <ScrollView
                        contentContainerStyle={styles.contentContainerStyle}

                    >

                        <View style={styles.imputContainer}>
                            <Text>state: {loggedIn.toString()}</Text>

                            <Text>Username:</Text>
                            <Input value={username} onChangeText={setUsername} placeholder="Enter your username" autoCapitalize="none" />
                            <Text>Password:</Text>
                            <Input value={password} onChangeText={setPassword} placeholder="Enter your password" secureTextEntry={true} autoCapitalize="none" />

                        </View>

                        <Button title="Login" onPress={handleLogin} />
                        <Separator />

                        <Button title="Register" onPress={() => navigation.navigate('Register')} />
                        <Separator />


                    </ScrollView>
                </KeyboardAvoidingView>


            )}
        </>



    );
};

export default LoginScreen;


const styles = StyleSheet.create({
    container: {
    },
    imputContainer: {
        width: 320
    },
    contentContainerStyle: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 0,
        backgroundColor: "#bee9f7"


    },
    separator: {
        marginVertical: 8,
        borderBottomColor: '#737373',
        borderBottomWidth: StyleSheet.hairlineWidth,
        width: 300
    },
    card: {
        backgroundColor: '#FFFFFF',
        borderRadius: 10,
        padding: 10,
        height: 150,
        marginTop: 10,
        width: 280,
    },
    card2: {
        backgroundColor: '#FFFFFF',
        borderRadius: 10,
        padding: 10,
        height: 400,
        marginTop: 10,
        width: 280,
    },
    cardTittle: {
        color: '#808080',
        fontSize: 22,
        marginBottom: 5,
    },
    header: {
        marginTop: 50,
        flexDirection: 'row',
        alignItems: 'center',
        padding: 20,
    },
    avatar: {
        width: 50,
        height: 50,
        borderRadius: 25,
    },
    info: {
        marginLeft: 20,
    },
    name: {
        fontSize: 24,
        fontWeight: 'bold',
    },
    username: {
        color: '#999',
        fontSize: 18,
    },
    appointmentItem: {
        // 添加其他样式属性
    },



});
