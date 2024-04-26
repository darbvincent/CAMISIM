import argparse
import gzip

def separate_paired_ends(input_file, output_r1, output_r2):
    with gzip.open(input_file, 'rt') as f_in, \
         gzip.open(output_r1, 'wt') as f_r1, \
         gzip.open(output_r2, 'wt') as f_r2:

        line_number = 0
        current_read = []

        for line in f_in:
            line_number += 1
            current_read.append(line)

            if line_number % 4 == 0:
                if '/1' in current_read[0]:
                    f_r1.write(''.join(current_read))
                elif '/2' in current_read[0]:
                    f_r2.write(''.join(current_read))
                else:
                    raise ValueError("Invalid read identifier in input file.")

                current_read = []

def main():
    parser = argparse.ArgumentParser(description="Separate paired-end reads from a FASTQ file.")
    parser.add_argument("-i", "--input", help="Input FASTQ file (gzipped)", required=True)
    parser.add_argument("-r1", "--output_r1", help="Output FASTQ file for read 1 (gzipped)", required=True)
    parser.add_argument("-r2", "--output_r2", help="Output FASTQ file for read 2 (gzipped)", required=True)
    args = parser.parse_args()

    separate_paired_ends(args.input, args.output_r1, args.output_r2)

if __name__ == "__main__":
    main()