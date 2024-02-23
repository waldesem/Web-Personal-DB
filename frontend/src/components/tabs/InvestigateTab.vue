<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { profileStore } from "@/store/profile";

const InvestigationForm = defineAsyncComponent(
  () => import("@components/forms/InvestigationForm.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const InvestigateDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/InvestigateDiv.vue")
);

const storeProfile = profileStore();
</script>

<template>
  <div class="py-3">
    <InvestigationForm
      v-if="
        (storeProfile.dataProfile.action === 'update' ||
          storeProfile.dataProfile.action === 'create') &&
        storeProfile.dataProfile.flag === 'investigation'
      "
    />
    <div v-else>
      <div v-if="storeProfile.dataProfile.inquisition.length">
        <CollapseDiv
          v-for="(item, idx) in storeProfile.dataProfile.inquisition"
          :key="idx"
          :id="'investigation' + idx"
          :idx="idx"
          :label="'Расследование #' + (idx + 1)"
        >
          <RowDivSlot :slotTwo="true" :print="true">
            <template v-slot:divTwo>
              <a
                href="#"
                title="Удалить"
                @click="
                  storeProfile.dataProfile.deleteItem(
                    props.item['id'].toString(),
                    'investigation'
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
                    'investigation',
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
          <RowDivSlot :label="'Информация'" :value="props.item['info']" />
          <RowDivSlot :label="'Сотрудник'" :value="props.item['officer']" />
          <RowDivSlot
            :label="'Дата'"
            :value="new Date(String(item['deadline'])).toLocaleDateString('ru-RU')"
          />
          <RowDivSlot :slotOne="true">
            <form
              class="form"
              enctype="multipart/form-data"
              role="form"
              @change="
                storeProfile.dataProfile.submitFile(
                  $event,
                  'investigation',
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
          @click="storeProfile.dataProfile.openForm('investigation', 'create')"
          >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
