import Vue from "vue";
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        loggedIn: false,
        token: localStorage.getItem('token') || '',
        username: localStorage.getItem('username') || ''
    },
    getters: {

    },
    actions: {
        // login start
        login(context, payload) {
            context.commit('login', payload)
        },
        // register start
        register(context, payload) {
            context.commit('register', payload)
        },
        // logout start
        logout(context) {
            context.commit('logout')
        },
    },
    mutations: {
        login(state, payload) {
            // checkers to see if data is valid
            if (String(payload.username).length == 0) {
                Vue.notify({
                    position: "top center",
                    group: "login",
                    text: "The username can't be blank 😔",
                    type: "error",
                })
                return(undefined);
            } else if (String(payload.password).length == 0) {
                Vue.notify({
                    position: "top center",
                    group: "login",
                    text: "The password can't be blank 😔",
                    type: "error",
                })
                return(undefined);
            }
            // POST request to /rest-author/login/
            axios.post("http://127.0.0.1:8000/rest-auth/login/", {
                username: payload.username,
                password: payload.password
            }, {
                headers: {'Content-Type': 'application/json',}
            }).then(function (response) {
                // if good response, user is logged in!
                if (response.status == 200) {
                    state.loggedIn = true;
                    state.token = response.data.key;
                    state.username = payload.username;
                    localStorage.setItem("token", response.data.key);
                    localStorage.setItem("loggedIn", true);
                    localStorage.setItem("username", payload.username);
                    Vue.notify({
                        position: "top center",
                        group: "login",
                        text: "Successfully logged into your account! 🙂",
                        type: "success",
                    })
                    // redirect user
                    window.setTimeout(function () {
                        window.location.href = "/dashboard/home";
                    }, 1000)
                }
                // uh oh, there's a problem
            }).catch(function (error) {
                if (error.response) {
                    Vue.notify({    
                        position: "top center",
                        group: "login",
                        text: `${error.response.data.non_field_errors[0]}` + " 😔",
                        type: "error",
                    });
                } else {
                    Vue.notify({
                        position: "top center",
                        group: "login",
                        text: `${error.response.data.password[0]}` + " 😔",
                        type: "error",
                    });
                }
                // set data
                state.loggedIn = false;
                state.token = "NONE";
                state.username = "";
                localStorage.setItem("token", "NONE");
                localStorage.setItem("loggedIn", false);
                localStorage.setItem("username", "");
            })
            return(undefined);
        },
        register(state, payload) {
            // data validation
            if (String(payload.username).length == 0) {
                Vue.notify({
                    position: "top center",
                    group: "login",
                    text: "The username can't be blank 😔",
                    type: "error",
                })
                return(undefined);
            } else if (String(payload.password1).length == 0) {
                Vue.notify({
                    position: "top center",
                    group: "login",
                    text: "The password can't be blank 😔",
                    type: "error",
                })
                return(undefined);
            }
        },
        logout(state) {

        }
    },
})