library(shiny)
library(readr)
library(dplyr)
library(ggplot2)
library(DT)

#-------------- 資料讀取分類 start -------------------------------
#分類
table <- read_csv("cocktails.csv")
#酸，材料有包含檸檬/酸相關的sour欄為1
sour <- table %>%
  filter(grepl("(Lemon.+)|((.+)?Sour(.+)?)",table$cocktails_name)|grepl("Lemon.+",table$ingredient_1)|grepl("Lemon.+",table$ingredient_2)|grepl("Lemon.+",table$ingredient_3)|grepl("Lemon.+",table$ingredient_4)|grepl("Lemon.+",table$ingredient_5)|grepl("Lemon.+",table$ingredient_6)|grepl("Lemon.+",table$ingredient_7)|grepl("Lemon.+",table$ingredient_8)|grepl("Lemon.+",table$ingredient_9)) %>%
  mutate(sour=1) %>%
  select(cocktails_name,sour)
#合併
table <-merge(table, sour, by = "cocktails_name", all = T)

#甜，材料有包含糖漿/甜相關的sweet欄為1
sweet <- table %>%
  filter(grepl("((.+)?Syrup(.+)?)|((.+)?Sweet)?)",table$cocktails_name)|grepl("(.+)?Syrup(.+)?",table$ingredient_1)|grepl("(.+)?Syrup(.+)?",table$ingredient_2)|grepl("(.+)?Syrup(.+)?",table$ingredient_3)|grepl("(.+)?Syrup(.+)?",table$ingredient_4)|grepl("(.+)?Syrup(.+)?",table$ingredient_5)|grepl("(.+)?Syrup(.+)?",table$ingredient_6)|grepl("(.+)?Syrup(.+)?",table$ingredient_7)|grepl("(.+)?Syrup(.+)?",table$ingredient_8)|grepl("(.+)?Syrup(.+)?",table$ingredient_9)) %>%
  mutate(sweet=1) %>%
  select(cocktails_name,sweet)
#合併
table <-merge(table, sweet, by = "cocktails_name", all = T)

#苦，材料有包含苦精相關的bitter欄為1
bitter <- table %>%
  filter(grepl("(.+)?Bitter(.+)?",table$cocktails_name)|grepl("(.+)?Bitter(.+)?",table$ingredient_1)|grepl("(.+)?Bitter(.+)?",table$ingredient_2)|grepl("(.+)?Bitter(.+)?",table$ingredient_3)|grepl("(.+)?Bitter(.+)?",table$ingredient_4)|grepl("(.+)?Bitter(.+)?",table$ingredient_5)|grepl("(.+)?Bitter(.+)?",table$ingredient_6)|grepl("(.+)?Bitter(.+)?",table$ingredient_7)|grepl("(.+)?Bitter(.+)?",table$ingredient_8)|grepl("(.+)?Bitter(.+)?",table$ingredient_9)) %>%
  mutate(bitter=1) %>%
  select(cocktails_name,bitter)
#合併
table <-merge(table, bitter, by = "cocktails_name", all = T)

#薄荷，材料有包含薄荷的mint欄為1
mint <- table %>%
  filter(grepl("(.+)?\\sMint(.+)?",table$cocktails_name)|grepl("(.+)?\\sMint(.+)?",table$ingredient_1)|grepl("(.+)?\\sMint(.+)?",table$ingredient_2)|grepl("(.+)?\\sMint(.+)?",table$ingredient_3)|grepl("(.+)?\\sMint(.+)?",table$ingredient_4)|grepl("(.+)?\\sMint(.+)?",table$ingredient_5)|grepl("(.+)?\\sMint(.+)?",table$ingredient_6)|grepl("(.+)?\\sMint(.+)?",table$ingredient_7)|grepl("(.+)?\\sMint(.+)?",table$ingredient_8)|grepl("(.+)?\\sMint(.+)?",table$ingredient_9)) %>%
  mutate(mint=1) %>%
  select(cocktails_name,mint)
#合併
table <-merge(table, mint, by = "cocktails_name", all = T)

#把table中的NA值取代為0
table[is.na(table)] <- 0
#--------------------資料讀取分類 end------------------------------



#-------------------shiny ui start---------------------------------

cocktails_flavor <- table %>% select(cocktails_name,sour,sweet,bitter,mint)

ui <- fluidPage(
  
  #ui標題
  titlePanel(strong("Recommend the Cocktails for You")),
  br(),
  
   #將版面分成兩塊(左)
  sidebarLayout(
    sidebarPanel(
      
  #複選input
  checkboxGroupInput("flavor", label = strong("Choose the flavor you like"), choices = names(cocktails_flavor) ,selected = names(cocktails_flavor) ),
  
  #心情拉桿input
  sliderInput("mood", "Your mood : 1(very bad)~10(very good)", value = 5, min = 0, max = 10),
    ),
  
  # verbatimTextOutput("summary"),
  
  #將版面分成兩塊(右)
  mainPanel(
    DT::dataTableOutput("cocktails"),
  )
  )
)
#-------------------shiny ui end---------------------------------



#-------------------shiny server start---------------------------
cocktails_name <- cocktails_flavor %>% select(cocktails_name)

server <- function(input, output, session) {
  # dataset <- reactive({
  #   get(input$dataset, cocktails_flavor)
  # })
  
  # output$summary <- renderPrint({
  #   summary(dataset())
  # })
  
  #顯示datatable
  output$cocktails <- DT::renderDataTable({
    DT::datatable(
      
      #依勾選可將該欄刪除不比較 
      #filter="top"可做為flavor為 1 或 0 的條件選擇
      #orderClasses == True 使點選該行時，會有灰底框住
      
      cocktails_flavor[, input$flavor],filter = 'top',options = list(orderClasses = TRUE))

  })
}

#-------------------shiny server end-----------------------------

#啟動shiny
shinyApp(ui=ui,server = server)
