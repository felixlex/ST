# кодирование
def hamming_encode(bits):
  bits.reverse()
  encoded_data = [0] * 7
  j = 0
  for i in range(1, 8):
    pos = i - 1
    if i == 1:
      encoded_data[pos] = bits[0] ^ bits[1] ^ bits[3]
    elif i == 2:
      encoded_data[pos] = bits[0] ^ bits[2] ^ bits[3]
    elif i == 4:
      encoded_data[pos] = bits[1] ^ bits[2] ^ bits[3]
    else:
      encoded_data[pos] = bits[j]
      j += 1
  return encoded_data

# декодирование
def hamming_decode(encoded_data, true_encoded):
  syndrome = [0] * 3
  syndrome[0] = encoded_data[0] ^ encoded_data[6] ^ encoded_data[
      4] ^ encoded_data[2]
  syndrome[1] = encoded_data[1] ^ encoded_data[5] ^ encoded_data[
      6] ^ encoded_data[2]
  syndrome[2] = encoded_data[3] ^ encoded_data[6] ^ encoded_data[
      5] ^ encoded_data[4]

  error_position = sum([2**i * syndrome[i] for i in range(3)])

  if error_position != 0:
    encoded_data[error_position - 1] ^= 1

  decoded_data = encoded_data
  if true_encoded == decoded_data:
    return 1
  else:
    return 0


# Пример использования
data_sequence = "1011"
d = list(map(int, list(data_sequence)))
encoded_sequence = hamming_encode(d)
print(f"Закодированная последовательность: {encoded_sequence}")

error_dict = {}

for i in range(1, 128):
  error = bin(i)[2:].zfill(7)
  encoded_sequence_with_error = []
  for j in range(7):
    if error[j] == '0':
      encoded_sequence_with_error.append(encoded_sequence[j])
    else:
      encoded_sequence_with_error.append(int(not encoded_sequence[j]))
  if error_dict.get(error.count('1')) is None:
    error_dict[error.count('1')] = [
        hamming_decode(encoded_sequence_with_error, encoded_sequence), 1
    ]
  else:
    error_dict[error.count('1')][0] += hamming_decode(
        encoded_sequence_with_error, encoded_sequence)
    error_dict[error.count('1')][1] += 1

  #error_dict[error.count('1')] += hamming_decode(encoded_sequence_with_error, encoded_sequence)

for k,v in error_dict.items():
  print(f'Кратность ошибки {k}   Кол-во обнаруженных ошибок {v[0]} Кол-во ошибок данной кратности  {v[1]}')
