import Vue from "vue";
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex)

export default new Vuex.Store({
    // state used for statuses
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
})

