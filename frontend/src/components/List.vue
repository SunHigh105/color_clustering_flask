<template>
  <div class="file-list">
    <h3>File List</h3>
        <div class="loading" v-show="loading">
          <div class="loading__inner">
            <h3>Clustering...</h3>
            <p>This process takes 1-2 minutes.</p>
            <img src="@/assets/icon_loader_f_ww_01_s1.gif">
          </div>
        </div>
        <ul class="file-list__content">
          <li v-for="(img, name) in imgList" v-bind:key="img.index">
            <ul class="file-list__content__info">
              <li><img v-bind:src="'/static/uploads/' + name"></li>
              <li>{{ name }}</li>
              <li><button type="button" @click="colorClustering(name)">Clustering</button></li>
            </ul>
            <div class="file-list__content__colorbar">
              <div v-for="row in img" v-bind:key="row.index" v-bind:style="'background-color: rgb(' + row[0] + ',' + row[1] + ',' + row[2] + ')'"></div>
            </div>
          </li>
        </ul>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      loading: false,
      imgList: {}
    }
  },
  mounted () {
    this.displayImg()
  },
  methods: {
    displayImg () {
      axios.post('http://localhost:5000/display_img')
        .then(response => {
          response.data.forEach(element => {
            this.$set(this.imgList, element, [])
          })
        })
        .catch(error => {
          console.log(error)
        })
    },
    colorClustering (fileName) {
      this.loading = true
      let params = new FormData()
      params.append('filename', fileName)
      axios.post('http://localhost:5000/color_clustering', params, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          if (fileName in this.imgList) {
            this.imgList[fileName].length = 0
            response.data['color_list'].forEach(row => {
              this.imgList[fileName].push(row)
            })
          }
          this.loading = false
          alert('Clustering Success!')
        })
        .catch(error => {
          this.loading = false
          alert('Clustering Failed.')
          console.log(error)
        })
    }
  }
}
</script>
