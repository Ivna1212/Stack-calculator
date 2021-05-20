<template>
    <div v-if="currentTask == n">
        <div>
            Чему равно значение выражения <span class="bigger">{{ task }}</span> ?<br>
            <span class="smaller">Если результатом является дробь, округлите вниз до целого.</span>
        </div>
        <div class="flex">
            <input type="text" v-model="answer" placeholder="Введите ответ" @keydown="$event.which == 13 && $emit('answer', answer)" ref="ans">
            <input type="button" value="Далее" @click="$emit('answer', answer)">
            <input type="button" :value="showAnswer ? 'Скрыть ответ' : 'Посмотреть ответ'" @click="showAnswer = !showAnswer" v-if="train">
        </div>
        <div v-if="showAnswer" style="margin-top: 8px">
            <div>Правильный ответ: {{ correctAnswer }}</div>
            <div v-if="hint">{{ hint }}</div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    props: ['task', 'n', 'currentTask', 'train', 'hint', 'correctAnswer'],
    data: () => ({
        answer: '',
        showAnswer: false,
        prevTask: null
    }),
    updated() {
        this.$refs.ans.focus();
        if (this.prevTask != this.task) {
            this.resetState();
            this.prevTask = this.task;
        }
    },
    methods: {
        resetState() {
            this.showAnswer = false;
            this.answer = '';
        }
    }
}
</script>

<style scoped>
input {
    margin: 0pt;
    margin-left: 10px;
}
input[type="text"] {
    width: 80%;
}
input[type="button"] {
    flex-grow: 1;
}
.flex {
    display: flex;
    margin-top: 8pt;
}
div {
    text-align: left;
}
.smaller {
    font-size: 12px;
}
.bigger {
    font-size: 24px;
}
</style>