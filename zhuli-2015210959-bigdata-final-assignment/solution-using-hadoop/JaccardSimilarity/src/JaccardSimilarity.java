import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DefaultStringifier;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class JaccardSimilarity extends
		org.apache.hadoop.mapreduce.Mapper<Object, Text, Text, DoubleWritable> {
	private static final String DELIMITER = "#";

	@Override
	protected void map(Object key, Text value, Context context)
			throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		StringTokenizer itr = new StringTokenizer(value.toString(), DELIMITER);
		int id1 = Integer.valueOf(itr.nextToken());
		String s1 = itr.nextToken();
		int id2 = Integer.valueOf(itr.nextToken());
		String s2 = itr.nextToken();

		Set<String> record1 = getSingleRecord(s1);
		Set<String> record2 = getSingleRecord(s2);
		Set<String> union = new HashSet<String>(record1);
		Set<String> intersection = new HashSet<>(record1);

		union.addAll(record2);
		intersection.retainAll(record2);
		double similarity = union.size() > 0 ? 1.0 * intersection.size()
				/ union.size() : 1.0;
		double threshold = DefaultStringifier.load(context.getConfiguration(),
				"threshold", DoubleWritable.class).get();

		if (similarity > threshold) {
			context.write(new Text(String.format("%d %d", id1, id2)),
					new DoubleWritable(similarity));
		}
	}

	private Set<String> getSingleRecord(String str) {
		String[] tokens = str.split("\\s");
		Set<String> set = new HashSet<String>();

		for (String token : tokens) {
			set.add(token);
		}
		return set;
	}

	public static void main(String[] args) throws IOException,
			ClassNotFoundException, InterruptedException {
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf, args)
				.getRemainingArgs();
		if (otherArgs.length != 3) {
			System.err
					.println("Usage: JaccardSimilarity <input> <output> <threshold>");
			System.exit(2);
		}

		String inputPath = otherArgs[0];
		String outputPath = otherArgs[1];
		double threshold = Double.valueOf(otherArgs[2]);
		DefaultStringifier.store(conf, new DoubleWritable(threshold), "threshold");

		Job job = new Job(conf, "Jaccard Similarity");
		job.setJarByClass(JaccardSimilarity.class);
		job.setMapperClass(JaccardSimilarity.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(DoubleWritable.class);
		FileInputFormat.addInputPath(job, new Path(inputPath));
		FileOutputFormat.setOutputPath(job, new Path(outputPath));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
