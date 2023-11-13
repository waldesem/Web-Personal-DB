<script setup lang="ts">

import { messageStore } from '@/store/messages';

const storeMessage = messageStore();

</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Сообщения'" />
    <div class="py-2">
      <div class="row justify-content-between">
        <div class="col">
          <p>
            <a href="#" class="link-success" @click="storeMessage.updateMessages('read')">
            Отметить прочитанными
          </a>
        </p>
        </div>
        <div class="col">
          <p>
            <a href="#" class="link-danger" @click="storeMessage.updateMessages('delete')">
              Удалить все сообщения
            </a>
          </p>
        </div>
      </div>
      <div class="py-2">
        <table class="table align-middle text-center no-bottom-border">
          <thead> 
            <tr>
              <th width="5%">#</th>
              <th width="15%">Категория</th>
              <th width="15%">Тема</th>
              <th>Сообщение</th>
              <th width="15%">Статус</th>
              <th width="10%">Дата</th>
            </tr>
          </thead>
          <tbody v-if="storeMessage.messageData.messages.length">
            <tr>
              <td colspan="6">
                <table v-for="message in storeMessage.messageData.messages" 
                       :key="message['id']" 
                       class="table table-hover align-middle text-center">
                  <tbody>
                    <tr>
                      <td width="5%">{{ `#${message['id']}` }}</td>
                      <td width="15%">{{ message['category'] }}</td>
                      <td width="15%">{{ message['title'] }}</td>
                      <td>{{ message['report'] }}</td>
                      <td width="15%">{{ message['status'] }}</td>
                      <td width="10%">{{ message['create'] }}</td>
                    </tr>
                  </tbody>
                </table>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="py-3">
      <nav v-if="storeMessage.messageData.hasPrev || storeMessage.messageData.hasNext">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !storeMessage.messageData.hasPrev }">
            <a class="page-link" href="#" 
              @click.prevent="storeMessage.messageData.currentPage -= 1;
                              storeMessage.updateMessages('all')">
                Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !storeMessage.messageData.hasNext }">
            <a class="page-link" href="#" 
              @click.prevent="storeMessage.messageData.currentPage += 1;
                              storeMessage.updateMessages('all')">
                Следующая
            </a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>