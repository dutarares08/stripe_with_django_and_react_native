import { StatusBar } from 'expo-status-bar';
import { Alert, Button, StyleSheet, Text, View } from 'react-native';
import { useState, useEffect } from "react"
// import { StripeProvider, useStripe } from '@stripe/stripe-react-native';
import { StripeProvider, useStripe } from '@stripe/stripe-react-native';
import Payment from './Payment';


export default function App() {

  const stripe = useStripe()
  const { initPaymentSheet, presentPaymentSheet } = useStripe();
  const [loading, setLoading] = useState(false);


  // const fetchPaymentSheetParams = async () => {
  //   const response = await fetch("http://192.168.101.12:8000/auth/for_payment/", {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //   });
  //   const { paymentIntent, ephemeralKey, customer} = await response.json();
  //   console.log("paymentIntent ",paymentIntent, "ephemeralKey ",ephemeralKey, "customer " ,customer)
  //   return {
  //     paymentIntent,
  //     ephemeralKey,
  //     customer,
  //   };
  // };

  // const initializePaymentSheet = async () => {
  //   const {
  //     paymentIntent,
  //     ephemeralKey,
  //     customer,
  //     publishableKey,
  //   } = await fetchPaymentSheetParams();

  //   const { error } = await initPaymentSheet({
  //     customerId: customer,
  //     customerEphemeralKeySecret: ephemeralKey,
  //     paymentIntentClientSecret: paymentIntent,
  //     merchantDisplayName: 'Merchant Name',
  //     googlePay: true,
  //     // Set `allowsDelayedPaymentMethods` to true if your business can handle payment
  //     //methods that complete payment after a delay, like SEPA Debit and Sofort.
  //     allowsDelayedPaymentMethods: true,
  //   });
  //   if (!error) {
  //     setLoading(true);
  //   }
  // };

  // const openPaymentSheet = async () => {
  //   console.log("called")
  //   const { error } = await presentPaymentSheet();

  //   if (error) {
  //     console.log("error")
  //     Alert.alert(`Error code: ${error.code}`, error.message);
  //   } else {
  //     console.log("no error")
  //     Alert.alert('Success', 'Your order is confirmed!');
  //   }
  // };


  // useEffect(() => {
  //   initializePaymentSheet();
  // }, []);

  const subscribeNow = async () => {
    const response = await fetch("http://192.168.101.12:8000/auth/create_customer/",
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    const { customer } = await response.json()

    
    console.log("customer ", customer)
    await create_subscription(customer)

  }

  const create_subscription = async (customer) => {
    const response = await fetch("http://192.168.101.12:8000/auth/create_subscription/",
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          priceId: "price_1LSQTwCFCYzaNOTCEyuSXzeC",
          customerId: customer,
        }),
      });

      const {subscriptionId, clientSecret} = await response.json()

      await initializePaymentSheet(customer, clientSecret, subscriptionId)
      
  }


const initializePaymentSheet = async (customer,clientSecret, subscriptionId ) => {

  console.log("client secret  ", clientSecret, subscriptionId)
    const { error } = await initPaymentSheet({
      customerId: customer,
      // customerEphemeralKeySecret: ephemeralKey,
      // paymentIntentClientSecret: subscriptionId,
      
      // setupIntentClientSecret:subscriptionId,
      paymentIntentClientSecret:clientSecret,
      
      merchantDisplayName: 'Merchant Name',
      googlePay: true,
      // Set `allowsDelayedPaymentMethods` to true if your business can handle payment
      //methods that complete payment after a delay, like SEPA Debit and Sofort.
      allowsDelayedPaymentMethods: true,
    });
    if (!error) {
      setLoading(true);
    }

    console.log("Eroriiiiiiii", error);
    await openPaymentSheet();

  };


  const openPaymentSheet = async () => {
    console.log("called")
    const { error } = await presentPaymentSheet();

    if (error) {
      console.log("error")
      Alert.alert(`Error code: ${error.code}`, error.message);
    } else {
      console.log("no error")
      Alert.alert('Success', 'Your order is confirmed!');
    }
  };


  return (
    <StripeProvider
      publishableKey="pk_live_51LQ6WDCFCYzaNOTCJZdZ6R90SGavrC2ZBKnTLs6dDqgQqSjBXC1CzmG1vzeIeSqGVF8iPWF8rScKFcs71dRoA9PF00eIVzvwlh"
    >
      <View style={styles.container}>
        <Text>Open up App.js to start working on your app!</Text>


        <Button onPress={() => subscribeNow()} title='Subscribe' />
        <Payment />
        <StatusBar style="auto" />
      </View>
    </StripeProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
