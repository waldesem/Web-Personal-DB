<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { profileStore } from "@/store/profile";

const PoligrafForm = defineAsyncComponent(
  () => import("@components/forms/PoligrafForm.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const PoligrafDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/InvestigateDiv.vue")
);

const storeProfile = profileStore();
</script>

<template>
  <div class="py-3">
    <PoligrafForm
      v-if="
        (storeProfile.dataProfile.action === 'update' ||
          storeProfile.dataProfile.action === 'create') &&
        storeProfile.dataProfile.flag === 'poligraf'
      "
    />
    <div v-else>
      <div v-if="storeProfile.dataProfile.pfo.length">
        <CollapseDiv
          v-for="(item, idx) in storeProfile.dataProfile.pfo"
          :key="idx"
          :id="'poligraf' + idx"
          :idx="idx"
          :label="'Полиграф #' + (idx + 1)"
        >
          <RowDivSlot :slotTwo="true" :print="true">
            <template v-slot:divTwo>
              <a
                href="#"
                title="Удалить"
                @click="
                  storeProfile.dataProfile.deleteItem(
                    props.item['id'].toString(),
                    'poligraf'
                  )
                "
              >
                <i class="bi bi-trash"></i> </a
              >&nbsp; &nbsp; &nbsp;
              <a
                href="#"
                title="Изменить"
                @click="
                  storeProfile.dataProfile.openForm(
                    'poligraf',
                    'update',
                    props.item['id'].toString(),
                    props.item
                  )
                "
              >
                <i class="bi bi-pencil-square"></i>
              </a>
            </template>
          </RowDivSlot>
          <RowDivSlot :label="'Тема'" :value="props.item['theme']" />
          <RowDivSlot :label="'Результат'" :value="props.item['results']" />
          <RowDivSlot :label="'Сотрудник'" :value="props.item['officer']" />
          <RowDivSlot
            :label="'Дата'"
            :value="new Date(String(item['deadline'])).toLocaleDateString('ru-RU')"
          />
          <RowDivSlot :slotOne="true" :print="true">
            <form
              class="form"
              enctype="multipart/form-data"
              role="form"
              @change="
                storeProfile.dataProfile.submitFile(
                  $event,
                  'poligraf',
                  props.item['id'].toString()
                )
              "
            >
              <input class="form-control" id="file" type="file" ref="file" multiple />
            </form>
          </RowDivSlot>
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <a
          class="btn btn-outline-primary"
          type="button"
          @click="storeProfile.dataProfile.openForm('poligraf', 'create')"
          >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
