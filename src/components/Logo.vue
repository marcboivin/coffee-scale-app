<template>
  <div id="logo-status">
    <h1>
      <b-icon-hexagon-fill
        v-b-tooltip.hover
        :variant="iconVariant"
        :title="tooltipMessage"
        :class="{ 'recording-animate': recording }"
      ></b-icon-hexagon-fill
      >&nbsp;Brew
    </h1>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Logo',
  computed: {
    ...mapState(['btEnabled', 'connected', 'recording']),
    iconVariant() {
      if (!this.btEnabled) {
        return 'danger'
      }
      if (!this.connected) {
        return 'warning'
      }
      return 'primary'
    },
    tooltipMessage() {
      return this.connected
        ? 'Scale is connected'
        : this.btEnabled
        ? 'Scale is NOT connected'
        : 'Bluetooth not available'
    }
  }
}
</script>

<style scoped lang="scss">
#logo-status {
  position: absolute;
  left: 3.8rem;
  top: 1.8rem;
  z-index: 100;
  background-color: #fff;
  border-radius: 0.2rem;
  padding: 0.5rem;
}
</style>
<style lang="css">
.recording-animate {
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.2;
  }
  100% {
    opacity: 1;
  }
}
</style>
