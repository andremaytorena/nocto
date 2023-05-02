import random
import csv
from Paths.paths import PATH_ADDRESSJIGGER_ADDRESSES

def start_jig():
    def jig(addressline):
        
        count = 0
        count_1 = 0
        count_letter = 0

        print(addressline)
        for i in range(2):



            verbs = ['Numbr', 'Door', 'House Num']
            verbs_2 = ['', 'no']
            random_letter = ['s', 'a']

            

            address = str(addressline)



            house_number = ""
            for i in address:
                if i.isdigit():
                    house_number = house_number + i

            # print(house_number)

            house_address_no_num = address.strip(house_number)



            word_list = house_address_no_num.split()
            number_of_words = len(word_list)

            if number_of_words == 1:
                print('1 word')


            elif number_of_words == 2:

                second_word = house_address_no_num.split(" ")[2]
                length_second_word = (len(second_word))
                length_second_word = length_second_word / 2
                length_second_word = (round(length_second_word))

                if count_letter == 0:
                    new_last_word = random_letter[count_letter] + '.' + second_word
                    

                    first_word = house_address_no_num.split(" ")[1]
                    first_word_length = (len(first_word))

                    random_length_num = random.randint(2,first_word_length-1)
                    random_letter_first = first_word[random_length_num]
                    first_half = first_word[:random_length_num]
                    second_half = first_word[random_length_num:]
                    

                    new_first_word = first_half + random_letter_first + second_half
                    

                    modified_addy_num = verbs[count] + ' ' + verbs_2[count_1] + '.' + house_number + ' ' +  new_first_word + ' '+ new_last_word
                    print(modified_addy_num)


                elif count_letter == 1:
                    new_last_word = '.' + second_word[:length_second_word]

                    first_word = house_address_no_num.split(" ")[1]
                    first_word_length = (len(first_word))

                    random_length_num = random.randint(2,first_word_length-1)
                    random_letter_first = first_word[random_length_num]
                    first_half = first_word[:random_length_num]
                    second_half = first_word[random_length_num:]
                    

                    new_first_word = first_half + random_letter_first + second_half

                    random_length_num1 = random.randint(2,first_word_length-1)
                    first_half = new_first_word[:random_length_num]
                    second_half = new_first_word[random_length_num:]

                    new = first_half + str(random_length_num1) + second_half

                    modified_addy_num = verbs[count] + ' ' + verbs_2[count_1] + '.' + house_number + ' ' +  new + ' '+ new_last_word
                    print(modified_addy_num)


            count_letter = count_letter + 1
            count = count + 1
            count_1 = count_1 + 1

    def start():
        with open(PATH_ADDRESSJIGGER_ADDRESSES) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                addressline = row[0]
                jig(addressline)


    start()