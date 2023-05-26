import { View, Text, KeyboardAvoidingView, ScrollView, StyleSheet, Button, GestureResponderEvent, Alert } from 'react-native'
import React, { useEffect, useLayoutEffect, useState } from 'react'
import { Image, Input } from '@rneui/themed';
import { CompositeNavigationProp, useNavigation } from '@react-navigation/native';
import { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import { TabStackParamList } from '../Navtor/TabNavtor';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootstackParamList } from '../Navtor/RootNavtor';
import Separator from '../component/Separator';
import { CheckBox } from '@rneui/base';
import axios from 'axios';


export type CustomerScreenNavigationProp = CompositeNavigationProp<

    BottomTabNavigationProp<TabStackParamList, 'Customer'>,
    NativeStackNavigationProp<RootstackParamList>
>



const RegisterScreen = () => {

    const navigation = useNavigation<CustomerScreenNavigationProp>();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmpassword, setConfirmPassword] = useState('');
    const [fullname, setFullname] = useState('');
    const [age, setAge] = useState<number>(0);
    const [gender, setGender] = useState('');
    const [phonenumber, setPhoneNumber] = useState('');
    const handleGenderChange = (value: string) => {
        setGender(value);
        console.log(value)
    }


    useLayoutEffect(() => {

    }, [])

    useEffect(() => {

    }, [])




    const handleRegister = async () => {
        try {

            if (password !== confirmpassword) {
                alert('Passwords do not match!');
                return;
            }
            if (!username) {
                alert('Please fill in username.');
                return;
            }
            if (!password) {
                alert('Please fill in password.');
                return;
            }
            if (!confirmpassword) {
                alert('Please fill in confirmpassword.');
                return;
            }
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
                username: username,
                password: password,
                customer: {
                    fullname: fullname,
                    age: age,
                    sex: gender,
                    phonenumber: phonenumber,
                },
            };



            // 发送注册请求
            const response2 = await axios.post(
                'http://192.168.110.91:8000/api/register_user/',
                data,
            );



            console.log('Register response:', JSON.stringify(response2.data));
            navigation.goBack();
            Alert.alert('', 'Registration completed.');
        } catch (error) {
            console.log(error);
        }
    };




    return (

        <KeyboardAvoidingView behavior="position" style={styles.contentContainerStyle}>
            <Image
                source={require('../assets/Register.png')}
                style={{ width: 430, height: 280, }}

            />

            <View
                style={styles.contentContainerStyle}

            >
                <ScrollView style={styles.imputContainer}>

                    <Text>Username:</Text>
                    <Input value={username} onChangeText={setUsername} placeholder="Enter your username" autoCapitalize="none"
                    />
                    <Text>Password:</Text>
                    <Input value={password} onChangeText={setPassword} placeholder="Enter your password" autoCapitalize="none" />
                    <Text>ConfirmPassword:</Text>
                    <Input value={confirmpassword} onChangeText={setConfirmPassword} placeholder="Enter your password" autoCapitalize="none" />
                    <Text>Fullname:</Text>
                    <Input value={fullname} onChangeText={setFullname} placeholder="Enter your fullname" autoCapitalize="none" />
                    <Text>Age:</Text>
                    <Input

                        value={age ? age.toString() : ""}
                        onChangeText={(text) => setAge(Number(text))}
                        placeholder="Enter your age"
                        keyboardType="numeric"
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
                    <Input value={phonenumber} onChangeText={setPhoneNumber} placeholder="Enter your fullname" />






                </ScrollView>



                <Button title="Register" onPress={handleRegister} />
                <Separator />
                <View style={{ height: 20 }} />



            </View>
        </KeyboardAvoidingView>



    )
}

export default RegisterScreen

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
    radioText: {
        marginHorizontal: 10,
    },


});