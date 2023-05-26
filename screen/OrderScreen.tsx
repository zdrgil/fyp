import { View, Text, ActivityIndicator, ScrollView, RefreshControl, StyleSheet, KeyboardAvoidingView, Button, TouchableOpacity, Platform, Alert } from 'react-native'
import React, { useEffect, useLayoutEffect, useState } from 'react'
import { CheckBox, Image, Input } from '@rneui/themed';
import DateTimePicker from '@react-native-community/datetimepicker';
import { useTailwind } from 'tailwind-rn/dist';
import Refresh from '../component/Refresh';
import Separator from '../component/Separator';
import { CompositeNavigationProp, useIsFocused, useNavigation } from '@react-navigation/native';
import { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import { TabStackParamList } from '../Navtor/TabNavtor';
import { RootstackParamList } from '../Navtor/RootNavtor';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Loading from '../component/Loading';
import axios from 'axios';
import RNPickerSelect from 'react-native-picker-select';
import { Icon } from '@rneui/base';

export type CustomerScreenNavigationProp = CompositeNavigationProp<
    BottomTabNavigationProp<TabStackParamList, 'Customer'>,
    NativeStackNavigationProp<RootstackParamList>
>

interface IClinic {
    id: number;
    clinicname: string;
    location: string;
    telnum: string;
    state: string;
    doctors: {
        id: number;
        name: string;
        state: string;
        clinic: number;
    };
}

const OrderScreen = ({ }: {}) => {
    const navigation = useNavigation<CustomerScreenNavigationProp>();
    const [loggedIn, setLoggedIn] = useState(false);
    const isFocused = useIsFocused();
    const [userData, setUserData] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [clinicdata, setClinicData] = useState<IClinic[]>([]);
    const [date, setDate] = useState(new Date());
    const [time, setTime] = useState(new Date());
    const [formattedDate, setFormattedDate] = useState('');
    const [formattedTime, setFormattedTime] = useState('');

    const [showDatePickerstate, setShowDatePicker] = useState(false);
    const [showTimePickerstate, setShowTimePicker] = useState(false);
    const [selectedClinic, setSelectedClinic] = useState<number | null>(null);
    const [doctorOptions, setDoctorOptions] = useState<any[]>([]);
    const [selectedDoctor, setSelectedDoctor] = useState<number | null>(null);
    const [fullname, setFullname] = useState('');
    const [age, setAge] = useState<number>(0);
    const [customer, setCustomer] = useState<number>(0);
    const [gender, setGender] = useState('');
    const [phonenumber, setPhoneNumber] = useState('');

    useLayoutEffect(() => {
        navigation.setOptions({
            headerShown: false,
        })
    }, [])
    const fetchClinic = async () => {
        try {
            const response = await axios.get<IClinic[]>('http://192.168.110.91:8000/api/clinics/');
            setClinicData(response.data);
            setLoading(false);
        } catch (error) {
            console.error(error);
        }
    };

    const fetchStoredData = async () => {
        try {
            const storedData = await AsyncStorage.getItem('usersData');
            if (storedData) {
                const parsedData = JSON.parse(storedData);
                setUserData(parsedData);
                if (parsedData.customer && parsedData.customer.fullname) {
                    setFullname(parsedData.customer.fullname);
                    setAge(parsedData.customer.age);
                    setGender(parsedData.customer.sex);
                    setPhoneNumber(parsedData.customer.phonenumber);
                    setCustomer(parsedData.customer.id);


                }
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
                fetchClinic();

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

    if (!clinicdata) {

    }


    const handleDateChange = (event: any, selectedDate: Date | undefined) => {
        const currentDate = selectedDate || date;
        setShowDatePicker(false);
        const formattedDate = currentDate.toISOString().split('T')[0];
        setFormattedDate(formattedDate);
        setDate(currentDate);
    };

    const handleTimeChange = (event: any, selectedTime: Date | undefined) => {
        const currentTime = selectedTime || time;
        setShowTimePicker(false);
        const hours = currentTime.getHours().toString().padStart(2, '0');
        const minutes = currentTime.getMinutes().toString().padStart(2, '0');
        const seconds = currentTime.getSeconds().toString().padStart(2, '0');

        const formattedTime = `${hours}:${minutes}:${seconds}`;
        setFormattedTime(formattedTime);
        console.log(formattedTime);
        setTime(currentTime)
    };

    const showDatePicker = () => {
        setShowDatePicker(true);

    };

    const showTimePicker = () => {
        setShowTimePicker(true);

    };

    const handleNameChange = (text: string) => {
        setFullname(text);
    };

    const handleGenderChange = (value: string) => {
        setGender(value);
    }
    const handlePNChange = (text: string) => {
        setPhoneNumber(text);
    };

    const handleClinicChange = (clinicId: number) => {
        const selectedClinic = clinicdata.find((clinic) => clinic.id === clinicId);
        const doctors = selectedClinic?.doctors || [];
        if (selectedClinic) {
            setDoctorOptions(
                Object.values(doctors).map((doctor) => ({
                    label: doctor.name,
                    value: doctor.id,
                }))
            );
        } else {
            setDoctorOptions([]);
        }
        setSelectedDoctor(null);
    };


    const handleRegisterAppointment = async () => {
        setLoading(true);
        try {
            const response1 = await axios.get('http://192.168.110.91:8000/api/get_csrf_token/');
            let newCSRFToken = response1.data.csrf_token;
            if (!fullname) {
                alert('Please fill in fullname.');
                return;
            }
            if (!age) {
                alert('Please fill in age.');
                return;
            }
            if (!gender) {
                alert('Please fill in gender.');
                return;
            }
            if (!phonenumber) {
                alert('Please fill in phonenumber.');
                return;
            }


            // 打印请求数据
            const data = {
                date: formattedDate,
                time: formattedTime,
                doctor: selectedDoctor,
                customer: customer,
                fullname: fullname,
                age: age,
                sex: gender,
                clinic: selectedClinic,
            };

            console.log('Request Data', data)
            // 发送注册请求
            const response2 = await axios.post(
                'http://192.168.110.91:8000/api/register_appointment/',
                data,
                {
                    headers: {
                        'X-CSRFToken': newCSRFToken, // 使用新的 CSRF Token
                    },
                }
            );
            Alert.alert('', 'Registration completed.');
            navigation.navigate('Login')
        } catch (error) {
            if (error.response && error.response.data && error.response.data.detail) {
                const errorMessage = error.response.data.detail;
                // 在界面上显示错误提示
                alert(errorMessage);
            } else {
                console.log(error);
            }
        }
    };




    return (
        <>
            {loggedIn ? (
                <KeyboardAvoidingView behavior="position" style={styles.contentContainerStyle}>
                    <Image
                        source={require('../assets/ap.png')}
                        style={{ width: 430, height: 280 }}
                    />
                    <View style={styles.contentContainerStyle}>
                        <ScrollView style={styles.imputContainer}>
                            <Text>Username:</Text>
                            <Input
                                value={userData.username}
                                editable={false}
                                placeholder="Enter your username"
                                autoCapitalize="none"
                            />
                            <Text>Datetime:</Text>


                            <View style={styles.pickerContainer}>
                                {Platform.OS === 'ios' && (
                                    <>

                                        <DateTimePicker

                                            value={date}
                                            mode="date"
                                            onChange={handleDateChange}
                                        />
                                        <DateTimePicker
                                            value={time}
                                            mode="time"
                                            onChange={handleTimeChange}
                                        />
                                    </>


                                )}

                                {Platform.OS === 'android' && (
                                    <>
                                        <Button onPress={showDatePicker} title="Open Date Picker" />
                                        <Button onPress={showTimePicker} title="Open Time Picker" />
                                        {showDatePickerstate && (
                                            <DateTimePicker
                                                value={date}
                                                mode="date"
                                                onChange={handleDateChange}
                                            />
                                        )}
                                        {showTimePickerstate && (
                                            <DateTimePicker
                                                value={time}
                                                mode="time"
                                                onChange={handleTimeChange}
                                            />
                                        )}
                                    </>
                                )}

                            </View>
                            <Text>Selected date: {date.toLocaleDateString()}</Text>
                            <Text >Selected time: {time.toLocaleTimeString()}</Text>
                            <Text>Doctor:</Text>
                            <RNPickerSelect
                                value={selectedClinic}
                                onValueChange={(value) => {
                                    setSelectedClinic(value);
                                    handleClinicChange(value);
                                }}
                                items={clinicdata.map((clinic) => ({
                                    label: clinic.clinicname,
                                    value: clinic.id,
                                }))}
                                style={pickerSelectStyles}
                                useNativeAndroidPickerStyle={false}
                            />
                            <Icon name="arrow-down" type="entypo" color={"#59C1CC"} />
                            <RNPickerSelect
                                value={selectedDoctor}
                                onValueChange={(value) => setSelectedDoctor(value)}
                                items={doctorOptions}
                                style={pickerSelectStyles}
                                useNativeAndroidPickerStyle={false}
                            />
                            <Text>Fullname:</Text>
                            <Input
                                value={fullname}
                                onChangeText={handleNameChange}
                                placeholder={"Enter your fullname"}
                                autoCapitalize="none"
                            />
                            <Text>Age:</Text>
                            <Input
                                value={age ? age.toString() : ""}
                                placeholder="Enter your age"
                                keyboardType="numeric"
                                onChange={(event) => {
                                    const text = event.nativeEvent.text;
                                    setAge(Number(text));
                                }}
                            />
                            <View style={styles.radioButtonContainer}>
                                <CheckBox
                                    title="Male"
                                    center
                                    checked={gender === 'male'}
                                    checkedIcon={"dot-circle-o"}
                                    uncheckedIcon={"circle-o"}
                                    onPress={() => handleGenderChange('male')}
                                />
                                <CheckBox
                                    title="Female"
                                    center
                                    checked={gender === 'female'}
                                    checkedIcon={"dot-circle-o"}
                                    uncheckedIcon={"circle-o"}
                                    onPress={() => handleGenderChange('female')}
                                />
                            </View>
                            <Text>Phone number:</Text>
                            <Input value={phonenumber} onChangeText={handlePNChange} placeholder="Enter your fullname" />
                        </ScrollView>
                        <Button title="Register" onPress={handleRegisterAppointment} />
                        <Separator />
                        <View style={{ height: 20 }} />
                    </View>
                </KeyboardAvoidingView>
            ) : (
                <KeyboardAvoidingView behavior="position" style={styles.contentContainerStyle}>
                    <Image
                        source={require('../assets/ap.png')}
                        style={{ width: 430, height: 280 }}
                    />
                    <ScrollView contentContainerStyle={styles.contentContainerStyle}>
                        <Text>Login first:</Text>
                        <Button title="Login" onPress={() => navigation.navigate('Login')} />
                        <Separator />
                        <Button title="Register" onPress={() => navigation.navigate('Register')} />
                        <Separator />
                    </ScrollView>
                </KeyboardAvoidingView>
            )}
        </>
    );
};

export default OrderScreen;

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
    radioButtonContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: 8,
        paddingHorizontal: 16,
        backgroundColor: '#fff',
        borderRadius: 4,
        borderWidth: 1,
        borderColor: '#ccc',
        marginBottom: 8,
    },
    separator: {
        marginVertical: 8,
        borderBottomColor: '#737373',
        borderBottomWidth: StyleSheet.hairlineWidth,
        width: 300,
    },
    pickerContainer: {
        flexDirection: 'row',
        marginTop: 8,
        paddingVertical: 8,
        backgroundColor: '#fff',
        borderRadius: 4,
        borderWidth: 1,
        borderColor: '#ccc',
        marginBottom: 8,
    },
});

const pickerSelectStyles = StyleSheet.create({
    inputIOS: {
        fontSize: 16,
        paddingHorizontal: 10,
        paddingVertical: 8,
        borderWidth: 0.5,
        borderColor: 'black',
        borderRadius: 8,
        color: 'black',
        paddingRight: 30,
        marginTop: 8,
        marginBottom: 8,
    },
    inputAndroid: {
        fontSize: 16,
        paddingHorizontal: 10,
        paddingVertical: 8,
        borderWidth: 0.5,
        borderColor: 'black',
        borderRadius: 8,
        color: 'black',
        paddingRight: 30,
        marginTop: 8,
        marginBottom: 8,
    },
});